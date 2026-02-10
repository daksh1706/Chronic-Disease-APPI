# src/advice_engine.py

def generate_advice(disease, risk):
    """
    disease: diabetes / heart / kidney / liver / asthma
    risk: percentage (0–100)
    returns: list of advice strings
    """

    advice = []

    if risk < 30:
        level = "Low"
    elif risk < 60:
        level = "Moderate"
    else:
        level = "High"

    advice.append(f"Risk Level: {level}")

    if disease == "diabetes":
        advice.extend([
            "Maintain a balanced diet with limited sugar intake",
            "Engage in regular physical activity",
            "Monitor blood glucose levels regularly",
            "Avoid excessive processed foods",
        ])

    elif disease == "heart":
        advice.extend([
            "Avoid smoking and excessive alcohol consumption",
            "Reduce salt and saturated fat intake",
            "Exercise at least 30 minutes daily",
            "Monitor blood pressure and cholesterol levels",
        ])

    elif disease == "kidney":
        advice.extend([
            "Stay well hydrated",
            "Limit salt and protein intake",
            "Monitor blood pressure regularly",
            "Avoid unnecessary painkillers",
        ])

    elif disease == "liver":
        advice.extend([
            "Avoid alcohol consumption",
            "Maintain a healthy weight",
            "Eat a liver-friendly diet",
            "Get liver function tests periodically",
        ])

    elif disease == "asthma":
        advice.extend([
            "Avoid known allergens and triggers",
            "Use prescribed inhalers properly",
            "Monitor breathing symptoms",
            "Exercise cautiously in clean environments",
        ])

    advice.append("Consult a healthcare professional for proper diagnosis.")

    return advice
