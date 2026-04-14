from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    preferred_name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True) # in kg
    height = models.FloatField(null=True, blank=True) # in cm
    cycle_length = models.IntegerField(default=28) # in days
    last_period_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

class PeriodTrackerEntry(models.Model):
    FLOW_CHOICES = [
        ('Light', 'Light'),
        ('Medium', 'Medium'),
        ('Heavy', 'Heavy'),
        ('Spotting', 'Spotting'),
        ('Unknown', 'Unknown'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='period_entries')
    entry_date = models.DateField()
    flow_level = models.CharField(max_length=32, choices=FLOW_CHOICES, default='Unknown')
    mood = models.JSONField(null=True, blank=True)
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_date', '-created_at']

    def __str__(self):
        return f"Period entry for {self.user.email} on {self.entry_date}"

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role.title()} message by {self.user.email} at {self.created_at}"

class BreastCancerScreenerHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='breast_cancer_entries')
    data = models.JSONField(null=True, blank=True)
    risk_score = models.FloatField(null=True, blank=True)
    recommendation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Breast cancer screener entry for {self.user.email} on {self.created_at:%Y-%m-%d}"

class CustomUserManager(BaseUserManager):
    """
    Custom manager where email is the unique identifier
    instead of username.
    """

    def create_user(self, email, full_name, password=None, **extra_fields):

        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, full_name, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model using email instead of username
    """

    username = None

    full_name = models.CharField(max_length=255)

    email = models.EmailField(
        _("email address"),
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email