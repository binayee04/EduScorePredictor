import streamlit as st
import pandas as pd
import joblib
import base64
import os

# 1. Load model and its feature names
@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    return model, model.feature_names_in_

# 2. Set custom background using CSS
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
    }}
    h1, h2, h3, h4, h5, h6, p {{
        color: white !important;
    }}
    .stSlider span {{
        color: white !important;
    }}
    .stSelectbox div, .stTextInput div {{
        color: black !important;
    }}
    .stButton > button {{
        background-color: black !important;
        color: white !important;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }}
    .prediction-box {{
        background-color: #111111dd;
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-top: 2rem;
        margin-bottom: 2rem;
        text-align: left;
        font-size: 16px;
        line-height: 1.6;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. Collect demographic inputs (Page 1)
def get_user_input_page1(form_data):
    form_data["gender"] = st.selectbox("Gender", ["female", "male"],
        index=["female", "male"].index(form_data["gender"]))

    form_data["race/ethnicity"] = st.selectbox("Race/Ethnicity",
        ["group A", "group B", "group C", "group D", "group E"],
        index=["group A", "group B", "group C", "group D", "group E"].index(form_data["race/ethnicity"]))
    
    return form_data

# 4. Collect academic info and predict (Page 2)
def get_user_input_page2(form_data):
    form_data["parental level of education"] = st.selectbox("Parental Level of Education", [
        "some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"
    ], index=[
        "some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"
    ].index(form_data["parental level of education"]))

    form_data["lunch"] = st.selectbox("Lunch Type", ["standard", "free/reduced"],
        index=["standard", "free/reduced"].index(form_data["lunch"]))

    form_data["test preparation course"] = st.selectbox("Test Preparation", ["none", "completed"],
        index=["none", "completed"].index(form_data["test preparation course"]))

    form_data["math score"] = st.slider("Math Score", 0, 100, form_data["math score"])
    form_data["reading score"] = st.slider("Reading Score", 0, 100, form_data["reading score"])
    form_data["writing score"] = st.slider("Writing Score", 0, 100, form_data["writing score"])

    return form_data

# 5. Predict the average score
def predict_score(input_data, model, model_features):
    df = pd.DataFrame([input_data])
    df_encoded = pd.get_dummies(df)
    df_encoded = df_encoded.reindex(columns=model_features, fill_value=0)
    return model.predict(df_encoded)[0]

# 6. Show prediction result nicely
def show_prediction_result(score):
    if score >= 85:
        emoji = "🌟"
        msg = "Excellent work. You're scoring high. Keep it up!"
        tip = "Maintain your study habits and help others too!"
    elif score >= 70:
        emoji = "💪"
        msg = "Good job. A bit more effort can push it even higher."
        tip = "Review your weak spots before tests."
    elif score >= 50:
        emoji = "📘"
        msg = "Decent score. Focus more on weak areas."
        tip = "Create a study schedule and stick to it."
    else:
        emoji = "⚠️"
        msg = "You might need help. Consider more study or tutoring."
        tip = "Don’t hesitate to ask for help or use learning resources."

    st.markdown(f"""
    <div class="prediction-box">
        <h4>🎯 <strong>Predicted Average Score: {score:.2f}</strong></h4>
        <p>{emoji} <strong>{msg}</strong></p>
        <p>💡 <em>Tip: {tip}</em></p>
    </div>
    """, unsafe_allow_html=True)

# 7. Main app logic
def main():
    st.set_page_config(page_title="Education Score Predictor", layout="centered")

    model, model_features = load_model()

    bg_path = "../assets/background.png"
    if os.path.exists(bg_path):
        set_background(bg_path)

    if "form_data" not in st.session_state:
        st.session_state.form_data = {
            "gender": "female",
            "race/ethnicity": "group A",
            "parental level of education": "some high school",
            "lunch": "standard",
            "test preparation course": "none",
            "math score": 70,
            "reading score": 70,
            "writing score": 70,
        }

    if "page" not in st.session_state:
        st.session_state.page = 1

    st.markdown("### 🎓 **Education Score Predictor**")
    st.markdown("#### 🎯 Enter Student Information to Predict Average Score")

    if st.session_state.page == 1:
        st.session_state.form_data = get_user_input_page1(st.session_state.form_data)
        if st.button("➡️ Next"):
            st.session_state.page = 2
            st.rerun()
    elif st.session_state.page == 2:
        st.session_state.form_data = get_user_input_page2(st.session_state.form_data)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Back"):
                st.session_state.page = 1
                st.rerun()

        with col2:
            if st.button("🎯 Predict"):
                score = predict_score(st.session_state.form_data, model, model_features)
                show_prediction_result(score)

        if st.button("🔁 Start Over"):
            st.session_state.page = 1
            st.session_state.form_data = {
                "gender": "female",
                "race/ethnicity": "group A",
                "parental level of education": "some high school",
                "lunch": "standard",
                "test preparation course": "none",
                "math score": 70,
                "reading score": 70,
                "writing score": 70,
            }
            st.rerun()

# Run the app
if __name__ == "__main__":
    main()
