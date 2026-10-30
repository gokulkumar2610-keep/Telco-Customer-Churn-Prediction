
import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# Load trained model
@st.cache_resource
def load_model():
    return joblib.load("model_files/churn_model.pkl")

model = load_model()

# Get original feature names
features = list(model.feature_names_in_)

st.title("📊 Telco Customer Churn Prediction")
st.write("Predict whether a telecom customer is likely to leave.")

# --- Sidebar threshold adjustment addition ---
st.sidebar.header("⚙️ Model Parameters")
threshold = st.sidebar.slider(
    "Decision Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.29,  # Defaulting to your business cost-tuned optimal threshold!
    step=0.01,
    help="Adjust the probability cutoff for flagging a customer as likely to churn. Lower thresholds catch more churners but increase false positives."
)

st.divider()

# Input form
with st.form("churn_form"):

    customer_data = {}

    categorical_options = {
        "gender": ["Male", "Female"],
        "SeniorCitizen": [0, 1],
        "Partner": ["Yes", "No"],
        "Dependents": ["Yes", "No"],
        "PhoneService": ["Yes", "No"],
        "MultipleLines": ["Yes", "No", "No phone service"],
        "InternetService": ["DSL", "Fiber optic", "No"],
        "OnlineSecurity": ["Yes", "No", "No internet service"],
        "OnlineBackup": ["Yes", "No", "No internet service"],
        "DeviceProtection": ["Yes", "No", "No internet service"],
        "TechSupport": ["Yes", "No", "No internet service"],
        "StreamingTV": ["Yes", "No", "No internet service"],
        "StreamingMovies": ["Yes", "No", "No internet service"],
        "Contract": ["Month-to-month", "One year", "Two year"],
        "PaperlessBilling": ["Yes", "No"],
        "PaymentMethod": [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    }

    numeric_options = {
        "tenure": (0, 72, 12),
        "MonthlyCharges": (0.0, 150.0, 70.0),
        "TotalCharges": (0.0, 10000.0, 1000.0)
    }

    for feature in features:

        if feature in categorical_options:
            customer_data[feature] = st.selectbox(
                feature,
                categorical_options[feature]
            )

        elif feature in numeric_options:
            low, high, default = numeric_options[feature]

            if feature == "tenure":
                customer_data[feature] = st.slider(
                    feature,
                    int(low),
                    int(high),
                    int(default)
                )
            else:
                customer_data[feature] = st.number_input(
                    feature,
                    min_value=float(low),
                    max_value=float(high),
                    value=float(default)
                )

        else:
            customer_data[feature] = st.text_input(feature)

    submit = st.form_submit_button("Predict Churn")

# Prediction
if submit:
    try:
        input_df = pd.DataFrame(
            [customer_data],
            columns=features
        )

        st.subheader("Prediction Result")

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            classes = list(model.classes_)

            churn_indices = [
                i for i, value in enumerate(classes)
                if str(value).strip().lower() in
                ["yes", "1", "true", "churn"]
            ]

            if churn_indices:
                churn_probability = float(probabilities[churn_indices[0]])
                
                # Apply the dynamically adjusted slider threshold
                is_churn = churn_probability >= threshold

                st.metric(
                    "Churn Probability",
                    f"{churn_probability * 100:.2f}%"
                )
                st.progress(churn_probability)

                if is_churn:
                    st.error(f"🚨 Customer is flagged as likely to Churn (Probability exceeds threshold of {threshold:.2f}).")
                else:
                    st.success(f"✅ Customer is likely to Stay (Probability is below threshold of {threshold:.2f}).")
        else:
            # Fallback for models without predict_proba
            prediction = model.predict(input_df)[0]
            if str(prediction).lower() in ["yes", "1", "true", "churn"]:
                st.error("Customer is likely to churn.")
            else:
                st.success("Customer is likely to stay.")

    except Exception as e:
        st.error(f"Prediction error: {e}")

st.divider()
st.caption("Telco Customer Churn Prediction | Machine Learning Project")
