from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pcos_screener.models import PCOSScreener


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """
    Get user dashboard data including welcome message and last PCOS result
    """
    user = request.user

    # Get the most recent PCOS screening result for this user
    last_pcos_result = None
    try:
        # For now, we'll return a mock result since the PCOSScreener model
        # needs to be updated to work with CustomUser
        # In a real implementation, you'd query the actual results
        last_pcos_result = {
            "probability": 35,
            "risk_level": "Low"
        }
    except Exception as e:
        # If no results exist, return None
        last_pcos_result = None

    # Create welcome message based on time of day
    from datetime import datetime
    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good Morning"
    elif current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    dashboard_data = {
        "username": user.username_display,
        "welcome_message": "Take control of your health journey today.",
        "last_pcos_result": last_pcos_result
    }

    return Response(dashboard_data)
