# apps/consultations/views.py
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ConsultationForm
from .models import (
    PregnancyStatus,
    SelfCareGoal,
    ProductInterest,
    ConsultationSubmission,
)


def consultations(request):
    # ----- Option lists for template loops (no inline Python in templates) -----
    def _fv(req, key):
        return req.POST.get(key, "") if req.method == "POST" else ""

    yesno_fields = [
        (
            "has_allergies",
            "Do You Have Any Allergies?",
            _fv(request, "has_allergies"),
            _fv(request, "has_allergies_details"),
        ),
        (
            "has_medical_conditions",
            "Do You Have Any Medical Conditions?",
            _fv(request, "has_medical_conditions"),
            _fv(request, "has_medical_conditions_details"),
        ),
        (
            "recent_major_health_event",
            "Have You Experienced Any Major Health Events Recently?",
            _fv(request, "recent_major_health_event"),
            _fv(request, "recent_major_health_event_details"),
        ),
        (
            "taking_meds_or_supplements",
            "Are You Taking Any Medications or Supplements?",
            _fv(request, "taking_meds_or_supplements"),
            _fv(request, "taking_meds_or_supplements_details"),
        ),
        (
            "sensitive_skin_or_dermatitis",
            "Do You Have Sensitive Skin or Dermatitis?",
            _fv(request, "sensitive_skin_or_dermatitis"),
            _fv(request, "sensitive_skin_or_dermatitis_details"),
        ),
    ]

    pregnancy_options = list(PregnancyStatus.choices)
    self_care_goals = list(SelfCareGoal.choices)
    product_interests = list(ProductInterest.choices)

    if request.method == "POST":
        form = ConsultationForm(request.POST)

        if form.is_valid():
            sub = form.save(raw_post=request.POST)  # persists raw_post safely

            # ---- Optional notification email (prints to console in dev) ----
            try:
                subject = "New consultation submission"
                lines = [
                    f"Name: {sub.first_name} {sub.last_name}".strip(),
                    f"Email: {sub.email or '-'}",
                    f"Phone: {sub.phone or '-'}",
                    f"DOB: {sub.dob or '-'}",
                    "",
                    "Selections:",
                    f"- Allergies: {sub.has_allergies}",
                    f"- Medical conditions: {sub.has_medical_conditions}",
                    f"- Major health event: {sub.recent_major_health_event}",
                    f"- Meds/supplements: {sub.taking_meds_or_supplements}",
                    f"- Sensitive skin: {sub.sensitive_skin_or_dermatitis}",
                    f"- Pregnancy status: {sub.get_pregnancy_status_display() or '-'}",
                    f"- Self-care goal: {sub.get_self_care_goal_display() or '-'}",
                    f"- Self-care goal (other): {sub.self_care_goals_other or '-'}",
                    f"- Product interest: {sub.get_product_interest_display() or '-'}",
                    "",
                    "Message:",
                    sub.message or "-",
                ]
                send_mail(
                    subject=subject,
                    message="\n".join(lines),
                    from_email=getattr(
                        settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"
                    ),
                    recipient_list=[
                        getattr(settings, "DEFAULT_TO_EMAIL", "owner@example.com")
                    ],
                    fail_silently=True,
                )
            except Exception:
                pass

            # Redirect to the Sent page
            return redirect("consultations:consultation_sent", pk=sub.pk)

        # Form invalid: show errors and keep user inputs “sticky”
        for field, errs in form.errors.items():
            for err in errs:
                messages.error(request, f"{field.replace('_',' ').title()}: {err}")

        return render(
            request,
            "consultations.html",
            {
                "form": form,
                "form_values": request.POST,  # use for sticky values in your custom HTML
                "yesno_fields": yesno_fields,
                "pregnancy_options": pregnancy_options,
                "self_care_goals": self_care_goals,
                "product_interests": product_interests,
            },
        )

    # GET
    form = ConsultationForm()
    return render(
        request,
        "consultations.html",
        {
            "form": form,
            "form_values": {},  # handy for adding sticky-value logic later
            "yesno_fields": yesno_fields,
            "pregnancy_options": pregnancy_options,
            "self_care_goals": self_care_goals,
            "product_interests": product_interests,
        },
    )


def consultation_sent(request, pk):
    # Detail page showing the just submitted data
    sub = get_object_or_404(ConsultationSubmission, pk=pk)
    return render(request, "consultation_sent.html", {"sub": sub})
