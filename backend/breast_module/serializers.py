from rest_framework import serializers
from .models import UserResponse, ImageUpload


# 📊 Questionnaire Serializer
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = [
            'age',
            'family_history',
            'lump',
            'pain',
            'size_change',
            'nipple_discharge',
            'skin_change',
            'smoking',
            'alcohol',
            'physical_activity'
        ]

    def validate_age(self, value):
        if value <= 0:
            raise serializers.ValidationError("Age must be positive")
        if value > 120:
            raise serializers.ValidationError("Age seems unrealistic")
        return value


# 🖼️ Image Upload Serializer
class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['image']  # 🚫 only allow image upload

    def validate_image(self, value):
        if not value.content_type.startswith('image'):
            raise serializers.ValidationError("File must be an image")

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image too large (max 5MB)")

        return value