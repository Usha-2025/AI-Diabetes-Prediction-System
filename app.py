import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

from utils.helper import (
    create_history_file,
    save_prediction
)

from utils.pdf_report import create_pdf

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Diabetes Prediction",
    page_icon="🩺",
    layout="wide"
)

# =========================================================
# LOAD CSS
# =========================================================

with open("style.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# =========================================================
# CREATE HISTORY FILE
# =========================================================

create_history_file()

# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load(
    "models/diabetes_model.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🩺 Navigation")

menu = st.sidebar.radio(
    "Go To",
    [
        "🏠 Dashboard",
        "🩺 Prediction",
        "📚 History",
        "🤖 Chatbot",
        "❤️ Insights"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        """
        <div style="
            background: linear-gradient(to right, #0077ff, #00b4ff);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
        ">

        <h1 style="
            color:white;
            text-align:center;
        ">
        🩺 Welcome to AI Diabetes Prediction System
        </h1>

        <p style="
            color:white;
            text-align:center;
            font-size:18px;
        ">
        Analyze diabetes risk using AI-powered healthcare analytics and smart health insights.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("📊 Healthcare Dashboard")

    st.caption(
        "AI Powered Diabetes Risk Analytics System"
    )

    history = pd.read_csv(
        "prediction_history.csv"
    )

    c1, c2, c3, c4 = st.columns(4)

    total_predictions = len(history)

    high_risk = len(
        history[
            history['Result'] == "High Risk"
        ]
    )

    moderate_risk = len(
        history[
            history['Result'] == "Moderate Risk"
        ]
    )

    low_risk = len(
        history[
            history['Result'] == "Low Risk"
        ]
    )

    with c1:

        st.metric(
            "Total Predictions",
            total_predictions
        )

    with c2:

        st.metric(
            "High Risk",
            high_risk
        )

    with c3:

        st.metric(
            "Moderate Risk",
            moderate_risk
        )

    with c4:

        st.metric(
            "Low Risk",
            low_risk
        )

    st.markdown("---")

    # =====================================================
    # CHARTS
    # =====================================================

    if not history.empty:

        # =================================================
        # PIE CHART
        # =================================================

        pie_chart = px.pie(

            history,

            names='Result',

            title='Risk Distribution',

            hole=0.5,

            color='Result',

            color_discrete_map={

                'Low Risk': '#00ff99',

                'Moderate Risk': '#ffaa00',

                'High Risk': '#ff4d4d'

            }
        )

        pie_chart.update_traces(
            textinfo='percent+label'
        )

        pie_chart.update_layout(

            paper_bgcolor="#031b34",

            font_color="white",

            title_font_size=24
        )

        st.plotly_chart(
            pie_chart,
            width='stretch'
        )

        st.markdown("---")

        # =================================================
        # BAR CHART
        # =================================================

        bar_chart = px.bar(

            history,

            x='Result',

            color='Result',

            title='Risk Category Analysis',

            color_discrete_map={

                'Low Risk': '#00ff99',

                'Moderate Risk': '#ffaa00',

                'High Risk': '#ff4d4d'

            }
        )

        bar_chart.update_layout(

            paper_bgcolor="#031b34",

            font_color="white"
        )

        st.plotly_chart(
            bar_chart,
            width='stretch'
        )

        st.markdown("---")

        # =================================================
        # BMI CHART
        # =================================================

        bmi_chart = px.histogram(

            history,

            x='BMI',

            nbins=10,

            title='BMI Distribution'
        )

        bmi_chart.update_layout(

            paper_bgcolor="#031b34",

            font_color="white"
        )

        st.plotly_chart(
            bmi_chart,
            width='stretch'
        )

        st.markdown("---")

        # =================================================
        # RISK TREND
        # =================================================

        if len(history) > 1:

            trend_chart = px.line(

                history,

                y='Risk',

                title='Risk Trend Analysis'
            )

            trend_chart.update_layout(

                paper_bgcolor="#031b34",

                font_color="white"
            )

            st.plotly_chart(
                trend_chart,
                width='stretch'
            )

        st.markdown("---")

        # =================================================
        # RECENT PREDICTIONS
        # =================================================

        st.subheader(
            "🕒 Recent Predictions"
        )

        recent = history.tail(5)

        st.dataframe(
            recent,
            width='stretch'
        )

# =========================================================
# PREDICTION
# =========================================================

elif menu == "🩺 Prediction":

    st.title("🩺 Diabetes Prediction")

    st.caption(
        "Enter patient medical details"
    )

    col1, col2 = st.columns(2)

    with col1:

        pregnancies = st.number_input(
            "Pregnancies",
            min_value=0,
            value=2
        )

        glucose = st.number_input(
            "Glucose",
            min_value=0,
            value=140
        )

        blood_pressure = st.number_input(
            "Blood Pressure",
            min_value=0,
            value=75
        )

        skin_thickness = st.number_input(
            "Skin Thickness",
            min_value=0,
            value=30
        )

    with col2:

        insulin = st.number_input(
            "Insulin",
            min_value=0.0,
            value=120.0
        )

        bmi = st.number_input(
            "BMI",
            min_value=0.0,
            value=32.5
        )

        dpf = st.number_input(
            "Diabetes Pedigree Function",
            min_value=0.0,
            value=0.45
        )

        age = st.number_input(
            "Age",
            min_value=1,
            value=35
        )

    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    if st.button("🔍 Predict Diabetes"):

        input_data = pd.DataFrame([{

            'Pregnancies': pregnancies,
            'Glucose': glucose,
            'BloodPressure': blood_pressure,
            'SkinThickness': skin_thickness,
            'Insulin': insulin,
            'BMI': bmi,
            'DiabetesPedigreeFunction': dpf,
            'Age': age

        }])

        input_data = scaler.transform(
            input_data
        )

        probability = model.predict_proba(
            input_data
        )

        risk = probability[0][1] * 100

        st.markdown("---")

        # =====================================================
        # RISK GAUGE
        # =====================================================

        st.subheader(
            "🎯 Diabetes Risk Gauge"
        )

        fig = go.Figure(go.Indicator(

            mode="gauge+number",

            value=risk,

            title={
                'text': "Risk Level"
            },

            gauge={

                'axis': {
                    'range': [0, 100]
                },

                'bar': {
                    'color': "#00b4ff"
                },

                'steps': [

                    {
                        'range': [0, 40],
                        'color': "green"
                    },

                    {
                        'range': [40, 70],
                        'color': "orange"
                    },

                    {
                        'range': [70, 100],
                        'color': "red"
                    }

                ]
            }
        ))

        fig.update_layout(

            paper_bgcolor="#031b34",

            font={'color': "white"}
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

        # =====================================================
        # RESULT
        # =====================================================

        if risk >= 70:

            result = "High Risk"

            st.error(
                f"🔴 High Diabetes Risk ({risk:.2f}%)"
            )

        elif risk >= 50:

            result = "Moderate Risk"

            st.warning(
                f"🟠 Moderate Diabetes Risk ({risk:.2f}%)"
            )

        else:

            result = "Low Risk"

            st.success(
                f"🟢 Low Diabetes Risk ({risk:.2f}%)"
            )

        save_prediction(
            pregnancies,
            glucose,
            blood_pressure,
            bmi,
            age,
            risk,
            result
        )

        st.markdown("---")

        # =====================================================
        # MODERN HEALTH ANALYSIS
        # =====================================================

        st.subheader(
            "📊 Health Analysis"
        )

        health_df = pd.DataFrame({

            "Category": [
                "Glucose",
                "Blood Pressure",
                "BMI"
            ],

            "Your Values": [
                glucose,
                blood_pressure,
                bmi
            ],

            "Normal Values": [
                100,
                80,
                24
            ]
        })

        health_chart = go.Figure()

        # USER VALUES
        health_chart.add_trace(

            go.Bar(

                x=health_df["Category"],

                y=health_df["Your Values"],

                name="Your Values",

                marker_color="#00b4ff"
            )
        )

        # NORMAL VALUES
        health_chart.add_trace(

            go.Bar(

                x=health_df["Category"],

                y=health_df["Normal Values"],

                name="Normal Values",

                marker_color="#00ff99"
            )
        )

        health_chart.update_layout(

            title="Health Analysis Comparison",

            barmode='group',

            paper_bgcolor="#031b34",

            plot_bgcolor="#031b34",

            font=dict(
                color="white"
            ),

            title_font_size=24
        )

        st.plotly_chart(
            health_chart,
            width='stretch'
        )

        st.markdown("---")

        # =====================================================
        # HEALTH SUMMARY
        # =====================================================

        st.subheader(
            "🩺 Health Summary"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Glucose",
                glucose
            )

        with c2:

            st.metric(
                "BMI",
                bmi
            )

        with c3:

            st.metric(
                "Risk",
                f"{risk:.2f}%"
            )

        # BMI STATUS
        if bmi < 18.5:

            bmi_status = "Underweight"

        elif bmi < 25:

            bmi_status = "Normal"

        elif bmi < 30:

            bmi_status = "Overweight"

        else:

            bmi_status = "Obese"

        st.info(
            f"📌 BMI Status: {bmi_status}"
        )

        st.markdown("---")

        # =====================================================
        # SMART HEALTH INSIGHTS
        # =====================================================

        st.subheader(
            "💡 Personalized Health Insights"
        )

        if glucose > 140:

            st.warning(
                "⚠ High glucose detected. Reduce sugar intake and monitor blood sugar regularly."
            )

        else:

            st.success(
                "✅ Glucose level looks stable."
            )

        if blood_pressure > 90:

            st.warning(
                "⚠ Blood pressure is higher than normal. Reduce salt intake and stress."
            )

        else:

            st.success(
                "✅ Blood pressure is within healthy range."
            )

        if bmi >= 30:

            st.error(
                "🔴 BMI indicates obesity. Daily exercise and healthy diet recommended."
            )

        elif bmi >= 25:

            st.warning(
                "🟠 You are overweight. Try maintaining healthy physical activity."
            )

        else:

            st.success(
                "✅ BMI looks healthy."
            )

        if age >= 45:

            st.info(
                "📌 Regular diabetes checkups are recommended after age 45."
            )

        if risk >= 70:

            st.error(
                "🚨 Immediate medical consultation is recommended."
            )

        elif risk >= 50:

            st.warning(
                "⚠ Moderate diabetes risk detected. Lifestyle improvements recommended."
            )

        else:

            st.success(
                "🎉 Your overall health indicators look stable."
            )

        st.markdown("---")

        # =====================================================
        # AI HEALTH SCORE
        # =====================================================

        st.subheader(
            "🧠 AI Health Score"
        )

        health_score = 100 - risk

        if health_score < 0:
            health_score = 0

        if health_score >= 80:

            health_status = "🟢 Excellent Health"

        elif health_score >= 60:

            health_status = "🟡 Moderate Health"

        elif health_score >= 40:

            health_status = "🟠 Health Needs Attention"

        else:

            health_status = "🔴 Critical Health Risk"

        score_fig = go.Figure(go.Indicator(

            mode="gauge+number",

            value=health_score,

            title={
                'text': "Health Score"
            },

            gauge={

                'axis': {
                    'range': [0, 100]
                },

                'bar': {
                    'color': "#00ff99"
                },

                'steps': [

                    {
                        'range': [0, 40],
                        'color': "red"
                    },

                    {
                        'range': [40, 70],
                        'color': "orange"
                    },

                    {
                        'range': [70, 100],
                        'color': "green"
                    }

                ]
            }
        ))

        score_fig.update_layout(

            paper_bgcolor="#031b34",

            font={'color': "white"}
        )

        st.plotly_chart(
            score_fig,
            width='stretch'
        )

        st.info(
            f"📌 {health_status}"
        )

        st.markdown("---")

        # =====================================================
        # PDF REPORT
        # =====================================================

        pdf_file = create_pdf(
            pregnancies,
            glucose,
            blood_pressure,
            bmi,
            age,
            risk,
            bmi_status
        )

        with open(pdf_file, "rb") as file:

            st.download_button(
                "📄 Download Report",
                file,
                file_name="diabetes_report.pdf"
            )

# =========================================================
# HISTORY
# =========================================================

elif menu == "📚 History":

    st.title("📚 Prediction History")

    history = pd.read_csv(
        "prediction_history.csv"
    )

    st.dataframe(
        history,
        width='stretch'
    )

# =========================================================
# CHATBOT
# =========================================================

elif menu == "🤖 Chatbot":

    st.title("🤖 AI Health Assistant")

    st.caption(
        "Ask diabetes and health related questions"
    )

    user_question = st.text_input(
        "Ask your question"
    )

    if st.button("💬 Ask AI"):

        question = user_question.lower()

        st.markdown(
            f"""
            <div class="chat-user">
            {user_question}
            </div>
            """,
            unsafe_allow_html=True
        )

        if "diabetes" in question:

            response = (
                "Diabetes is a chronic condition that affects how your body processes blood sugar."
            )

        elif "symptoms" in question:

            response = (
                "Common symptoms include frequent urination, excessive thirst, fatigue and blurred vision."
            )

        elif "food" in question:

            response = (
                "Healthy foods include vegetables, whole grains, fruits and high-fiber foods."
            )

        elif "exercise" in question:

            response = (
                "Walking, jogging, yoga and cycling are very beneficial for diabetes management."
            )

        elif "bmi" in question:

            response = (
                "BMI helps determine whether your body weight is healthy according to your height."
            )

        elif "glucose" in question:

            response = (
                "High glucose levels may indicate diabetes risk and should be monitored regularly."
            )

        elif "blood pressure" in question:

            response = (
                "Maintaining healthy blood pressure reduces diabetes-related complications."
            )

        elif "sleep" in question:

            response = (
                "Good sleep improves insulin sensitivity and overall health."
            )

        elif "stress" in question:

            response = (
                "Stress can increase blood sugar levels and negatively affect diabetes management."
            )

        else:

            response = (
                "Please ask diabetes, BMI, glucose, exercise, food or health related questions."
            )

        st.markdown(
            f"""
            <div class="chat-ai">
            🤖 {response}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# INSIGHTS
# =========================================================

elif menu == "❤️ Insights":

    st.title("❤️ Health Insights")

    st.success(
        "Healthy lifestyle reduces diabetes risk."
    )

    st.write("✅ Exercise Daily")
    st.write("✅ Drink More Water")
    st.write("✅ Avoid Sugar")
    st.write("✅ Maintain Healthy BMI")