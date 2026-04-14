from datetime import datetime
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, UserProfile, PeriodTrackerEntry, ChatMessage, BreastCancerScreenerHistory
from .serializers import (
    CustomUserSerializer,
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    PeriodTrackerEntrySerializer,
    ChatMessageSerializer,
    BreastCancerScreenerHistorySerializer,
    PCOSScreenerSerializer,
)
from pcos_screener.models import PCOSScreener
from period_tracker.models import SymptomLog
from period_tracker.models import Cycle


# User registration endpoint
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_setup_view(request):
    """
    Catch health details from the React Onboarding form
    """
    # Check if the user already has a profile, otherwise create one
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # partial=True allows users to skip fields if they want
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint that returns JWT tokens
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_serializer = CustomUserSerializer(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Get current user profile and profile settings
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_serializer = CustomUserSerializer(request.user)
    profile_serializer = UserProfileSerializer(profile)
    return Response(
        {
            'user': user_serializer.data,
            'profile': profile_serializer.data,
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def period_tracker_log_view(request):
    try:
        data = request.data
        user = request.user

        flow = data.get("flow_level")
        entry_date = datetime.strptime(
            data.get("entry_date"), "%Y-%m-%d"
        ).date()

        #reset cycle on period
        # get last cycle
        last_cycle = Cycle.objects.filter(user=user).order_by("-start_date").first()

        # only create new cycle if:
        # - flow indicates period
        # - AND it's NOT consecutive day
        if flow in ["Light", "Medium", "Heavy"]:
            if not last_cycle:
                Cycle.objects.create(
                    user=user,
                    start_date=entry_date,
                    end_date=entry_date
                )
            else:
                gap = (entry_date - last_cycle.start_date).days

                # 👉 ONLY create new cycle if gap is big (new period)
                if gap > 7:
                    Cycle.objects.create(
                        user=user,
                        start_date=entry_date,
                        end_date=entry_date
            )


        log, created = SymptomLog.objects.update_or_create(
            user=user,
            date=entry_date,
            defaults={
                "flow": flow,
                "mood": ", ".join(data.get("mood", [])),
                "cramps": 1 if "Cramps" in data.get("symptoms", []) else 0,
                "fatigue": 1 if "Fatigue" in data.get("symptoms", []) else 0,
                "acne": "Acne" in data.get("symptoms", []),
                "headache": "Headache" in data.get("symptoms", []),
                "bloating": "Bloating" in data.get("symptoms", []),
                "breast_tenderness": "Tender Breasts" in data.get("symptoms", []),
            }
        )

        return Response({
            "id": log.id,
            "entry_date": log.date,
            "mood": data.get("mood", []),
            "symptoms": data.get("symptoms", [])
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def period_tracker_history_view(request):
    logs = SymptomLog.objects.filter(user=request.user).order_by("-date")

    data = []

    for log in logs:
        data.append({
            "id": log.id,
            "entry_date": log.date,

            "flow_level": log.flow if log.flow else "None",

            "mood": list(set(log.mood.split(", "))) if log.mood else [],

            "symptoms": [
                s for s in [
                    "Cramps" if log.cramps else None,
                    "Fatigue" if log.fatigue else None,
                    "Acne" if log.acne else None,
                    "Headache" if log.headache else None,
                    "Bloating" if log.bloating else None,
                    "Tender Breasts" if log.breast_tenderness else None,
                ] if s
            ]
        })

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_message_view(request):
    serializer = ChatMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history_view(request):
    messages = ChatMessage.objects.filter(user=request.user)
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def breast_cancer_history_view(request):
    if request.method == 'POST':
        serializer = BreastCancerScreenerHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    entries = BreastCancerScreenerHistory.objects.filter(user=request.user)
    serializer = BreastCancerScreenerHistorySerializer(entries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pcos_history_view(request):
    results = PCOSScreener.objects.filter(user=request.user).order_by('-created_at')
    serializer = PCOSScreenerSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)