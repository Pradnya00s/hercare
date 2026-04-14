from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile, PeriodTrackerEntry, ChatMessage, BreastCancerScreenerHistory
from pcos_screener.models import PCOSScreener

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'email', 'created_at')
        read_only_fields = ('id', 'created_at')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                              email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include email and password')

        attrs['user'] = user
        return attrs
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['preferred_name', 'age', 'weight', 'height', 'cycle_length', 'last_period_date']


class PeriodTrackerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodTrackerEntry
        fields = ['id', 'entry_date', 'flow_level', 'mood', 'symptoms', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class BreastCancerScreenerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BreastCancerScreenerHistory
        fields = ['id', 'data', 'risk_score', 'recommendation', 'created_at']
        read_only_fields = ['id', 'created_at']


class PCOSScreenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCOSScreener
        fields = ['id', 'age', 'weight', 'height', 'irregular_cycles', 'acne', 'hirsutism', 'created_at']
        read_only_fields = ['id', 'created_at']