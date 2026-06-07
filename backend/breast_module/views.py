from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from .serializers import UserResponseSerializer, ImageUploadSerializer
from .ml_model import predict_image


@api_view(['POST'])
def full_assessment(request):
    # Validate questionnaire
    user_serializer = UserResponseSerializer(data=request.data)

    # Validate image
    image_serializer = ImageUploadSerializer(data=request.data)

    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=400)

    if not image_serializer.is_valid():
        return Response(image_serializer.errors, status=400)

    # Save both
    user_instance = user_serializer.save()
    image_instance = image_serializer.save()

    try:
        image_path = image_instance.image.path

        # 🧠 ML prediction
        ml_result = predict_image(image_path)

        # 📊 Questionnaire scoring (reuse your logic)
        data = user_serializer.validated_data
        score = 0

        if data['age'] > 40:
            score += 2
        if data['family_history']:
            score += 3
        if data['lump']:
            score += 5
        if data['pain']:
            score += 2
        if data['size_change']:
            score += 3
        if data['nipple_discharge']:
            score += 4
        if data['skin_change']:
            score += 4
        if data['smoking']:
            score += 2
        if data['alcohol']:
            score += 1

        if data['physical_activity'] == "low":
            score += 2
        elif data['physical_activity'] == "medium":
            score += 1

        # 🔥 Combine ML + questionnaire
        ml_label = ml_result.get("result")
        confidence = ml_result.get("confidence", 0)

        if ml_label == "Malignant" and confidence > 70:
            final_risk = "High"
        elif score > 10 or confidence > 60:
            final_risk = "Medium"
        else:
            final_risk = "Low"

        return Response({
            "ml_result": ml_label,
            "confidence": confidence,
            "questionnaire_score": score,
            "final_risk": final_risk
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)