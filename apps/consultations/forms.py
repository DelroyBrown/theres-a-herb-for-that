# apps\consultations\forms.py
from django import forms
from .models import (
    ConsultationSubmition,
    PregnancyStatus,
    SelfCareGoal,
    ProductInterest,
)


def _yesno_coerce(val):
    # Map yes/no strings to boolean
    if val is None:
        return None
    v = str(val).strip().lower()
    if v == "yes":
        return True
    if v == "no":
        return False
    return None


YES_NO_CHOICES = (
    ("yes", "Yes"),
    ("no", "No"),
)


class ConsultationForm(forms.ModelForm):
    # Contact
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=50, required=False)
    dob = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    # yes/no checkboxes
    has_allergies = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=_yesno_coerce,
        required=False,
        empty_value=None,
        widget=forms.RadioSelect,
        label="Do You Have Any Allergies?",
    )
    has_medical_conditions = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=_yesno_coerce,
        required=False,
        empty_value=None,
        widget=forms.RadioSelect,
        label="Do You Have Any Medical Conditions?",
    )
    recent_major_health_event = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=_yesno_coerce,
        required=False,
        empty_value=None,
        widget=forms.RadioSelect,
    )
    taking_meds_or_supplements = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=_yesno_coerce,
        required=False,
        empty_value=None,
        widget=forms.RadioSelect,
    )
    sensitive_skin_or_dermatitis = forms.TypedChoiceField(
        choices=YES_NO_CHOICES,
        coerce=_yesno_coerce,
        required=False,
        empty_value=None,
        widget=forms.RadioSelect,
    )

    # Enums from the models
    pregnancy_status = forms.ChoiceField(
        choices=[("", "---------")] + list(PregnancyStatus.choices),
        required=False,
    )
    self_care_goals = forms.ChoiceField(
        choices=[("", "---------")] + list(SelfCareGoal.choices),
        required=False,
    )
    self_care_goals_other = forms.CharField(
        max_length=200,
        required=False,
        help_text="If other, please specify.",
    )

    product_interests = forms.ChoiceField(
        choices=[("", "---------")] + list(ProductInterest.choices),
        required=False,
    )

    # Message
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5}),
        required=False,
    )

    # Consents
    consent_understand_not_medical = forms.BooleanField(
        required=False,
        label="I understand that this consultation does not constitute medical advice.",
    )
    consent_review_answers = forms.BooleanField(
        required=False,
        label="I consent to having my answers reviewed by a qualified professional.",
    )
    consent_read_safety_info = forms.BooleanField(
        required=False,
        label="I have read the safety information provided.",
    )
    consent_use_products_safely = forms.BooleanField(
        required=False,
        label="I agree to use any recommended products safely and as directed.",
    )

    class Meta:
        model = ConsultationSubmition
        fields = [
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

    def save(self, commit=True, raw_post=None):
        """
        Allow the view to pass the raw POST dict so we can persist it into the models raw_post field without re-parsing
        """
        instance = super().save(commit=False)
        if raw_post is not None:
            instance.raw_post = dict(raw_post)
        if commit:
            instance.save()
        return instance
