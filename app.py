from question_engine import ask_questions
from predict import predict_disease
from advice_engine import generate_advice

def main():
    print("\n🩺 Chronic Disease Risk Assessment\n")

    disease = input(
        "Select disease (diabetes / heart / asthma): "
    ).strip().lower()

    user_input = ask_questions(disease)

    risk, accuracy = predict_disease(disease, user_input)

    print(f"\n📊 {disease.capitalize()} Risk Score: {risk:.2f}%")

    if accuracy is not None:
        print(f"✅ Model Accuracy (test set): {accuracy:.2f}%")

        if accuracy >= 80:
            print("🔎 Prediction Confidence: High")
        elif accuracy >= 65:
            print("🔎 Prediction Confidence: Moderate")
        else:
            print("🔎 Prediction Confidence: Low")
    else:
        print("⚠️ Model accuracy not available")
        print("🔎 Prediction Confidence: Unknown")

    advice = generate_advice(disease, risk)

    print("\n📝 Advice:")
    for a in advice:
        print("-", a)

if __name__ == "__main__":
    main()
