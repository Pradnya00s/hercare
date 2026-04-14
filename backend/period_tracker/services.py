from .models import SymptomLog, LifestyleLog
from collections import defaultdict
from datetime import timedelta
from .models import Cycle
from datetime import datetime
from .ml_model import predict_irregularity
from django.utils import timezone

# 📊 Get user cycles sorted
def get_user_cycles(user):
    cycles = Cycle.objects.filter(user=user).order_by("start_date")
    return list(cycles)


# 📈 Calculate average cycle length
def get_average_cycle_length(cycles):
    lengths = []

    for i in range(1, len(cycles)):
        diff = (cycles[i].start_date - cycles[i - 1].start_date).days
        lengths.append(diff)

    if not lengths:
        return 28  # default

    return sum(lengths) / len(lengths)


# 🔮 Predict next period date
def predict_next_period(user):
    cycles = get_user_cycles(user)

    if not cycles:
        return None

    avg_cycle = get_average_cycle_length(cycles)
    last_cycle = cycles[-1]

    predicted_date = last_cycle.start_date + timedelta(days=int(avg_cycle))

    return {
        "predicted_start_date": predicted_date,
        "avg_cycle_length": round(avg_cycle, 1),
    }


# 🥚 Ovulation window (approx: 14 days before next period)
def predict_ovulation(user):
    prediction = predict_next_period(user)

    if not prediction:
        return None

    next_period = prediction["predicted_start_date"]

    ovulation_day = next_period - timedelta(days=14)

    fertile_start = ovulation_day - timedelta(days=2)
    fertile_end = ovulation_day + timedelta(days=2)

    return {
        "ovulation_day": ovulation_day,
        "fertile_window_start": fertile_start,
        "fertile_window_end": fertile_end,
        "confidence": "medium",  # can improve later
    }



# 📊 Get symptom logs
def get_symptom_logs(user):
    return SymptomLog.objects.filter(user=user).order_by("date")


# 🌿 Get lifestyle logs
def get_lifestyle_logs(user):
    return LifestyleLog.objects.filter(user=user).order_by("date")


# 🔍 Detect recurring symptom patterns
def detect_symptom_patterns(user):
    logs = get_symptom_logs(user)

    symptom_counts = defaultdict(int)

    for log in logs:
        if log.cramps:
            symptom_counts["cramps"] += 1
        if log.fatigue:
            symptom_counts["fatigue"] += 1
        if log.acne:
            symptom_counts["acne"] += 1
        if log.headache:
            symptom_counts["headache"] += 1

    patterns = []

    for symptom, count in symptom_counts.items():
        if count >= 3:
            patterns.append(f"Frequent {symptom} detected")

    return patterns


# 🔗 Correlate symptoms with lifestyle
def correlate_lifestyle(user):
    symptoms = get_symptom_logs(user)
    lifestyle = get_lifestyle_logs(user)

    correlations = []

    for s in symptoms:
        for l in lifestyle:
            if s.date == l.date:
                if s.fatigue and l.sleep_hours and l.sleep_hours < 6:
                    correlations.append("Fatigue linked to low sleep")

                if s.cramps and l.stress_level and l.stress_level >= 4:
                    correlations.append("Cramps may be linked to high stress")

    return list(set(correlations))


# 📈 Health score (0–100)
def calculate_health_score(user):
    cycles = get_user_cycles(user)
    symptoms = get_symptom_logs(user)

    score = 100

    # cycle regularity
    if len(cycles) >= 3:
        lengths = []
        for i in range(1, len(cycles)):
            diff = (cycles[i].start_date - cycles[i - 1].start_date).days
            lengths.append(diff)

        avg = sum(lengths) / len(lengths)

        for length in lengths:
            if abs(length - avg) > 7:
                score -= 10

    # symptom severity
    for log in symptoms:
        if log.cramps:
            score -= 2
        if log.fatigue:
            score -= 2

    return max(score, 0)


# 🧠 Generate insights (main function)
def generate_insights(user):
    patterns = detect_symptom_patterns(user)
    correlations = correlate_lifestyle(user)
    health_score = calculate_health_score(user)

    insights = []

    # pattern insights
    for p in patterns:
        insights.append(p)

    # lifestyle insights
    for c in correlations:
        insights.append(c)

    # health score interpretation
    if health_score > 80:
        insights.append("Your cycle health looks good overall.")
    elif health_score > 60:
        insights.append("Some irregularities detected. Monitor your cycle.")
    else:
        insights.append("Consider consulting a healthcare professional.")

    return {
        "health_score": health_score,
        "insights": insights
    }


def predict_cycle(user):
    cycles = Cycle.objects.filter(user=user).order_by("start_date")

    if len(cycles) < 2:
        return {
            "error": "Not enough data to predict cycle"
        }

    lengths = [c.cycle_length for c in cycles if c.cycle_length]

    # ✅ SAFE handling
    if len(lengths) == 0:
        avg_cycle_length = 28
        variance = 5   # safe default
    else:
        avg_cycle_length = sum(lengths) / len(lengths)
        variance = max(lengths) - min(lengths)

    last_cycle = cycles.last()
    last_start = last_cycle.start_date

    next_period = last_start + timedelta(days=int(avg_cycle_length))
    ovulation_day = next_period - timedelta(days=14)

    fertile_start = ovulation_day - timedelta(days=2)
    fertile_end = ovulation_day + timedelta(days=2)

    # ✅ DO NOT recalculate variance again
    confidence = max(50, 100 - variance * 2)

    return {
        "next_period_date": next_period,
        "ovulation_date": ovulation_day,
        "fertile_window": {
            "start": fertile_start,
            "end": fertile_end
        },
        "confidence_score": round(confidence, 2)
    }

def get_cycle_phase(user):
    cycles = Cycle.objects.filter(user=user).order_by("start_date")

    if not cycles.exists():
        return {"error": "No cycle data available"}

    last_cycle = cycles.order_by("-start_date").first()
    today = timezone.localdate()

    # Days since last period start
    days_since_start = (today - last_cycle.start_date).days + 1

    # 🔍 DEBUG HERE
    print("ALL CYCLES:", list(cycles.values_list("start_date", flat=True)))
    print("LAST CYCLE START:", last_cycle.start_date)
    print("TODAY:", today)
    print("DAYS SINCE START:", days_since_start)

    # Use average cycle length if available
    lengths = [c.cycle_length for c in cycles if c.cycle_length]
    avg_cycle_length = int(sum(lengths) / len(lengths)) if lengths else 28

    # Phase logic
    if days_since_start <= 5:
        phase = "Menstrual"
        message = "Your period phase. Rest and recovery are important."
    elif days_since_start <= 13:
        phase = "Follicular"
        message = "Energy rising. Good time to start new tasks."
    elif days_since_start <= 16:
        phase = "Ovulation"
        message = "Peak fertility window. You may feel more social and confident."
    else:
        phase = "Luteal"
        message = "Progesterone rising. Focus on calm routines and self-care."

    # Safety (if cycle too long)
    if days_since_start > avg_cycle_length + 5:
        phase = "Irregular"
        message = "Your cycle seems delayed. Consider tracking closely or consulting a doctor."

    return {
        "phase": phase,
        "day_in_cycle": days_since_start,
        "avg_cycle_length": avg_cycle_length,
        "message": message
    }

def detect_irregularities(user):
    cycles = Cycle.objects.filter(user=user).order_by("start_date")

    if len(cycles) < 3:
        return {"message": "Not enough data for irregularity detection"}

    lengths = [c.cycle_length for c in cycles if c.cycle_length]
    if not lengths:
        return {
            "error": "No cycle length data available"
        }


    avg = sum(lengths) / len(lengths)
    variance = max(lengths) - min(lengths)

    issues = []

    # 🚨 Irregular cycle length
    if variance > 7:
        issues.append("Cycle length varies significantly")

    # 🚨 Too long cycles
    if avg > 35:
        issues.append("Cycles are longer than normal")

    # 🚨 Too short cycles
    if avg < 21:
        issues.append("Cycles are shorter than normal")

    # 🚨 Missed cycle (gap detection)
    gaps = []
    for i in range(1, len(cycles)):
        gap = (cycles[i].start_date - cycles[i-1].start_date).days
        gaps.append(gap)

    if any(g > 45 for g in gaps):
        issues.append("Possible missed or delayed periods")

    # 🧠 Confidence score
    confidence = min(95, 60 + len(lengths) * 5)

    return {
        "is_irregular": len(issues) > 0,
        "issues": issues,
        "average_cycle_length": round(avg, 2),
        "cycle_variation": variance,
        "confidence": confidence
    }

def detect_irregularity_ml(user):
    cycles = Cycle.objects.filter(user=user).order_by("start_date")

    if len(cycles) < 3:
        return {
            "error": "Not enough data for ML prediction"
        }

    lengths = [c.cycle_length for c in cycles if c.cycle_length]

    if not lengths:
        return {
            "error": "Insufficient cycle length data"
        }

    # 📊 Feature extraction
    avg = sum(lengths) / len(lengths)
    variation = max(lengths) - min(lengths)

    # 📅 Gap calculation
    gaps = []
    for i in range(1, len(cycles)):
        gap = (cycles[i].start_date - cycles[i-1].start_date).days
        gaps.append(gap)

    max_gap = max(gaps) if gaps else avg

    # 🤖 ML prediction
    result = predict_irregularity(avg, variation, max_gap)

    return {
        "average_cycle_length": round(avg, 2),
        "cycle_variation": variation,
        "max_gap": max_gap,
        "is_irregular": result["is_irregular"],
        "confidence": result["confidence"],
        
    }

