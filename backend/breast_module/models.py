from django.db import models


class UserResponse(models.Model):
    age = models.IntegerField()

    family_history = models.BooleanField()
    lump = models.BooleanField()
    pain = models.BooleanField()
    size_change = models.BooleanField()
    nipple_discharge = models.BooleanField()
    skin_change = models.BooleanField()

    smoking = models.BooleanField()
    alcohol = models.BooleanField()

    PHYSICAL_ACTIVITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    physical_activity = models.CharField(max_length=10, choices=PHYSICAL_ACTIVITY_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response {self.id} - Age {self.age}"


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    
    # 🧠 Store prediction result
    result = models.CharField(max_length=20, blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.result}"