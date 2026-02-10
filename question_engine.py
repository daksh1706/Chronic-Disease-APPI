# src/question_engine.py

# --------------------------------
# DISEASE KEY MAPPING
# --------------------------------
DISEASE_NAME_MAP = {
    "diabetes": "Diabetes",
    "heart": "Heart Disease",
    "asthma": "Asthma",
}

# --------------------------------
# SYMPTOM & RISK QUESTIONS
# --------------------------------
disease_questions = {

    "Diabetes": [
        {"question": "Do you feel excessively thirsty?", "feature": "polydipsia"},
        {"question": "Do you urinate more frequently than usual?", "feature": "polyuria"},
        {"question": "Do you feel unusually hungry?", "feature": "polyphagia"},
        {"question": "Do you experience unexplained weight loss?", "feature": "weight_loss"},
        {"question": "Do you often feel fatigued?", "feature": "fatigue"},
        {"question": "Do you have blurred vision?", "feature": "blurred_vision"},
        {"question": "Do you have a family history of diabetes?", "feature": "family_history"},
    ],

    "Heart Disease": [
        {"question": "Do you experience chest pain or discomfort?", "feature": "chest_pain"},
        {"question": "Do you feel shortness of breath during exertion?", "feature": "shortness_of_breath"},
        {"question": "Do you have a history of high blood pressure?", "feature": "hypertension"},
        {"question": "Do you have high cholesterol?", "feature": "high_cholesterol"},
        {"question": "Do you smoke cigarettes?", "feature": "smoking"},
        {"question": "Do you feel palpitations or irregular heartbeat?", "feature": "palpitations"},
        {"question": "Do you have a family history of heart disease?", "feature": "family_history"},
    ],

    "Asthma": [
        {"question": "Do you experience wheezing?", "feature": "wheezing"},
        {"question": "Do you feel shortness of breath?", "feature": "shortness_of_breath"},
        {"question": "Do you have chest tightness?", "feature": "chest_tightness"},
        {"question": "Do you experience coughing at night or early morning?", "feature": "night_cough"},
        {"question": "Do symptoms worsen with exercise?", "feature": "exercise_induced"},
        {"question": "Do you have a history of allergies?", "feature": "allergy_history"},
    ],
}

# --------------------------------
# NUMERIC / CLINICAL INPUTS
# --------------------------------
disease_numeric_tests = {

    "Diabetes": [
        {"name": "Age (years)", "feature": "age"},
        {"name": "Body Mass Index (BMI)", "feature": "bmi"},
        {"name": "Fasting Blood Glucose (mg/dL)", "feature": "glucose"},
        {"name": "HbA1c (%)", "feature": "hba1c"},
    ],

    "Heart Disease": [
        {"name": "Age (years)", "feature": "age"},
        {"name": "Resting Blood Pressure (mmHg)", "feature": "resting_bp"},
        {"name": "Total Cholesterol (mg/dL)", "feature": "cholesterol"},
        {"name": "Maximum Heart Rate Achieved", "feature": "max_hr"},
    ],

    "Asthma": [
        {"name": "Age (years)", "feature": "age"},
        {"name": "Peak Expiratory Flow (PEF)", "feature": "pef"},
    ],
}

# --------------------------------
# QUESTION ENGINE
# --------------------------------
def ask_questions(disease):
    """
    Ask symptom + numeric questions for a disease.
    disease: diabetes / heart / kidney / liver / asthma
    Returns: dict of feature:value
    """

    if disease not in DISEASE_NAME_MAP:
        raise ValueError(f"Unknown disease: {disease}")

    disease_key = DISEASE_NAME_MAP[disease]
    user_data = {}

    print(f"\n🩺 Answer the following questions for {disease_key}:\n")

    # Yes / No questions
    for q in disease_questions[disease_key]:
        while True:
            ans = input(q["question"] + " (Yes/No): ").strip().lower()
            if ans in ("yes", "no"):
                user_data[q["feature"]] = 1 if ans == "yes" else 0
                break
            print("Please answer Yes or No.")

    # Numeric inputs
    print("\n📊 Enter clinical values (press Enter to skip):\n")
    for test in disease_numeric_tests.get(disease_key, []):
        while True:
            val = input(f"{test['name']}: ").strip()
            if val == "":
                user_data[test["feature"]] = None
                break
            try:
                user_data[test["feature"]] = float(val)
                break
            except ValueError:
                print("Please enter a valid number or press Enter to skip.")

    return user_data
