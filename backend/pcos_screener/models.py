from django.db import models
from accounts.models import CustomUser


class PCOSScreener(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    irregular_cycles = models.BooleanField(default=False)
    acne = models.BooleanField(default=False)
    hirsutism = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Screener data for {self.user.email}"
