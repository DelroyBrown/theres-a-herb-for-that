# apps\consultations\models.py
from django.db import models


class PregnancyStatus(models.TextChoices):
    PREGNANT = "pregnant", "Pregnant"
    BREASTFEEDING = "breastfeeding", "Breast Feeding"
    TRYING_TO_CONCEIVE = "trying to conceive", "Trying To Conceive"
    NONE = "none", "None of the Above"


class SelfCareGoal(models.TextChoices):
    RELAX_STRESS = "relax_stress", "Relaxation & Stress Relief"
    BETTER_SLEEP = "better_sleep", "Better Sleep"
    SKINCARE = "skincare", "Skincare & Nourishment"
    ENERGY_FOCUS = "energy_focus", "More Energy / Focus"
    EMOTIONAL_BALANCE = "emotional_balance", "Emotional Balance"
    OTHER = "other", "Other"


class ProductInterest(models.TextChoices):
    HERBAL_BEVERAGES = "herbal_beverages", "Herbal Beverages"
    FACIAL_CARE = "facial_care", "Facial Care"
    ORAL_CARE = "oral_care", "Oral Care"
    BODY_CARE = "body_care", "Body Care"
    OPEN_TO_ANYTHING = "open_to_anything", "Open to Anything"


class ConsultationSubmition(models.Model):
    # Contact
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    dob = models.DateField(blank=True, null=True)

    # Health & safety (yes/no radios)
    has_allergies = models.BooleanField(null=True, default=False)
    has_medical_conditions = models.BooleanField(null=True, blank=True, default=False)
    recent_major_health_event = models.BooleanField(
        null=True, blank=True, default=False
    )
    taking_meds_or_supplements = models.BooleanField(
        null=True, blank=True, default=False
    )
    sensitive_skin_or_dermatitis = models.BooleanField(
        null=True, blank=True, default=False
    )

    # Pregnancy/Breastfeeding/TTC
    pregnancy_status = models.CharField(
        max_length=50,
        choices=PregnancyStatus.choices,
        default=PregnancyStatus.NONE,
    )
    # Self-care goals
    self_care_goals = models.CharField(
        max_length=50,
        choices=SelfCareGoal.choices,
        blank=True,
    )
    self_care_goals_other = models.CharField(
        max_length=200, blank=True, help_text="If other, please specify."
    )

    # Product references
    product_interests = models.CharField(
        max_length=50,
        choices=ProductInterest.choices,
        blank=True,
    )

    # optional message
    message = models.TextField(blank=True)

    # Consent checkboxes
    consent_understand_not_medical = models.BooleanField(null=True, blank=True)
    consent_review_answers = models.BooleanField(null=True, blank=True)
    consent_read_safety_info = models.BooleanField(null=True, blank=True)
    consent_use_products_safely = models.BooleanField(null=True, blank=True)

    # Safety net: full POST payload for audit/debug
    raw_post = models.JSONField(default=dict, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class META:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["-submitted_at"]),
            models.Index(fields=["email"]),
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        base = f"{self.first_name} {self.last_name}".strip() or "Ananymous"
        return f"{base} - {self.submitted_at:%Y-%m-%d %H:%M}"
    

