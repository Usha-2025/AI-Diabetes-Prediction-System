import pandas as pd
import os

def create_history_file():

    if not os.path.exists(
        "prediction_history.csv"
    ):

        history_df = pd.DataFrame(columns=[
            'Pregnancies',
            'Glucose',
            'BloodPressure',
            'BMI',
            'Age',
            'Risk',
            'Result'
        ])

        history_df.to_csv(
            "prediction_history.csv",
            index=False
        )

def save_prediction(
    pregnancies,
    glucose,
    blood_pressure,
    bmi,
    age,
    risk,
    result
):

    data = pd.DataFrame([{
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'BMI': bmi,
        'Age': age,
        'Risk': risk,
        'Result': result
    }])

    data.to_csv(
        "prediction_history.csv",
        mode='a',
        header=False,
        index=False
    )