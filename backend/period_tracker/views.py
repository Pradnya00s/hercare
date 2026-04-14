from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import get_cycle_phase, detect_irregularities, detect_irregularity_ml
from rest_framework import status
from .models import SymptomLog, Cycle


from .models import Cycle
from .services import (
    predict_next_period,
    predict_ovulation,
    detect_irregularities,
    generate_insights,
)


# 🩸 Add cycle
@csrf_exempt
def add_cycle(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)

        user = request.user  # assumes logged-in user

        cycle = Cycle.objects.create(
            user=user,
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            cycle_length=data.get("cycle_length"),
            period_length=data.get("period_length"),
        )

        return JsonResponse({
            "message": "Cycle added",
            "id": cycle.id
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    user = request.user

    logs = SymptomLog.objects.filter(user=user).order_by("-date")

    data = []

    for log in logs:

        symptoms = []   # ✅ define BEFORE dict

        if log.cramps:
            symptoms.append("Cramps")
        if log.fatigue:
            symptoms.append("Fatigue")
        if log.acne:
            symptoms.append("Acne")
        if log.headache:
            symptoms.append("Headache")
        if log.bloating:
            symptoms.append("Bloating")
        if log.breast_tenderness:
            symptoms.append("Tender Breasts")

        data.append({
            "id": log.id,
            "entry_date": log.date,

            "flow_level": getattr(log, "flow", "None"),

            "mood": log.mood.split(", ") if log.mood else [],

            "symptoms": symptoms   # ✅ now valid
        })
    return Response(data)


# 🧠 Insights
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_insights(request):
    user = request.user

    insights = generate_insights(user)

    return Response(insights)


from .services import predict_cycle


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_prediction(request):
    result = predict_cycle(request.user)
    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phase(request):
    result = get_cycle_phase(request.user)
    return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_irregularity_analysis(request):
    user = request.user

    # Rule-based result
    rule_result = detect_irregularities(user)

    # ML-based result
    ml_result = detect_irregularity_ml(user)

    return Response({
        "rule_based": rule_result,
        "ml_based": ml_result
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_log(request, id):
    try:
        log = SymptomLog.objects.get(id=id, user=request.user)

        # 🧠 check if this log is a cycle start
        cycle = Cycle.objects.filter(
            user=request.user,
            start_date=log.date
        ).first()

        # delete log
        log.delete()

        # ❗ ALSO delete cycle if it matches start date
        if cycle:
            cycle.delete()

        return Response({"message": "Deleted successfully"}, status=200)

    except SymptomLog.DoesNotExist:
        return Response({"error": "Log not found"}, status=404)