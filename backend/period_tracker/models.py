from django.db import models
from django.conf import settings


class Cycle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    cycle_length = models.IntegerField(null=True, blank=True)
    period_length = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.start_date}"


class SymptomLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date = models.DateField()
    flow = models.CharField(max_length=20, default="None")

    cramps = models.BooleanField(default=False)
    fatigue = models.BooleanField(default=False)
    bloating = models.BooleanField(default=False)
    breast_tenderness = models.BooleanField(default=False)
    acne = models.BooleanField(default=False)
    headache = models.BooleanField(default=False)

    mood = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} - {self.date}"


class LifestyleLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date = models.DateField()

    sleep_hours = models.FloatField(null=True, blank=True)
    stress_level = models.IntegerField(null=True, blank=True)
    activity_level = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date}"