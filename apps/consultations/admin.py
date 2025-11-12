from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import csv
import json

from .models import ConsultationSubmition


@admin.register(ConsultationSubmition)
class ConsultationSubmitionAdmin(admin.ModelAdmin):
    """Admin interface for ConsultationSubmition records."""

    # ---------- LIST VIEW ----------
    list_display = (
        "submitted_at",
        "full_name",
        "email",
        "phone",
        "pregnancy_status_display",
        "self_care_goals_display",
        "product_interests_display",
        "has_allergies",
        "has_medical_conditions",
        "recent_major_health_event",
        "taking_meds_or_supplements",
        "sensitive_skin_or_dermatitis",
    )
    list_filter = (
        "pregnancy_status",
        "self_care_goals",
        "product_interests",
        "has_allergies",
        "has_medical_conditions",
        "recent_major_health_event",
        "taking_meds_or_supplements",
        "sensitive_skin_or_dermatitis",
        "submitted_at",
    )
    search_fields = ("first_name", "last_name", "email", "phone", "message")
    ordering = ("-submitted_at",)
    date_hierarchy = "submitted_at"
    list_per_page = 50

    # ---------- DETAIL VIEW ----------
    fieldsets = (
        (
            "Contact Information",
            {"fields": (("first_name", "last_name"), ("email", "phone"), "dob")},
        ),
        (
            "Health & Safety",
            {
                "fields": (
                    "has_allergies",
                    "has_medical_conditions",
                    "recent_major_health_event",
                    "taking_meds_or_supplements",
                    "sensitive_skin_or_dermatitis",
                    "pregnancy_status",
                )
            },
        ),
        (
            "Goals & Preferences",
            {
                "fields": (
                    "self_care_goals",
                    "self_care_goals_other",
                    "product_interests",
                    "message",
                )
            },
        ),
        (
            "Consent",
            {
                "fields": (
                    "consent_understand_not_medical",
                    "consent_review_answers",
                    "consent_read_safety_info",
                    "consent_use_products_safely",
                )
            },
        ),
        (
            "Raw Submission Data",
            {
                "classes": ("collapse",),
                "fields": ("submitted_at", "raw_post_pretty"),
            },
        ),
    )

    readonly_fields = ("submitted_at", "raw_post_pretty")
    actions = ["export_as_csv"]

    # ---------- DISPLAY HELPERS ----------
    @admin.display(description="Full Name")
    def full_name(self, obj):
        name = f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        return name or "—"

    @admin.display(description="Pregnancy Status", ordering="pregnancy_status")
    def pregnancy_status_display(self, obj):
        # Choice display for pregnancy_status
        return getattr(
            obj, "get_pregnancy_status_display", lambda: obj.pregnancy_status
        )()

    @admin.display(description="Self-care Goal", ordering="self_care_goals")
    def self_care_goals_display(self, obj):
        # Choice display for self_care_goals
        return getattr(
            obj, "get_self_care_goals_display", lambda: obj.self_care_goals
        )()

    @admin.display(description="Product Interest", ordering="product_interests")
    def product_interests_display(self, obj):
        # Choice display for product_interests
        return getattr(
            obj, "get_product_interests_display", lambda: obj.product_interests
        )()

    @admin.display(description="Raw POST (formatted)")
    def raw_post_pretty(self, obj):
        """Pretty-print JSON data in the admin."""
        if not obj.raw_post:
            return "—"
        try:
            data = json.dumps(obj.raw_post, indent=2, ensure_ascii=False)
        except Exception:
            return "Invalid JSON"
        return mark_safe(f"<pre style='white-space:pre-wrap'>{data}</pre>")

    # ---------- EXPORT AS CSV ----------
    def export_as_csv(self, request, queryset):
        """Export selected submissions to CSV."""
        meta = self.model._meta
        field_names = [
            "submitted_at",
            "first_name",
            "last_name",
            "email",
            "phone",
            "dob",
            "has_allergies",
            "has_medical_conditions",
            "recent_major_health_event",
            "taking_meds_or_supplements",
            "sensitive_skin_or_dermatitis",
            "pregnancy_status",
            "self_care_goals",
            "self_care_goals_other",
            "product_interests",
            "message",
            "consent_understand_not_medical",
            "consent_review_answers",
            "consent_read_safety_info",
            "consent_use_products_safely",
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="{meta.model_name}_export.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, f, "") for f in field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = "Export selected submissions as CSV"
