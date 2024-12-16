import joblib
import pandas as pd

label_encoder = joblib.load("model/label_encoder.joblib")
scaler = joblib.load("model/scaler_variable.joblib")

model_columns = [
    "Marital_status", "Application_mode", "Application_order", "Course",
    "Daytime_evening_attendance", "Previous_qualification", "Previous_qualification_grade",
    "Nacionality", "Mothers_qualification", "Fathers_qualification",
    "Mothers_occupation", "Fathers_occupation", "Admission_grade",
    "Displaced", "Educational_special_needs", "Debtor", "Tuition_fees_up_to_date",
    "Gender", "Scholarship_holder", "Age_at_enrollment", "International",
    "Curricular_units_1st_sem_credited", "Curricular_units_1st_sem_enrolled",
    "Curricular_units_1st_sem_evaluations", "Curricular_units_1st_sem_approved",
    "Curricular_units_1st_sem_grade", "Curricular_units_1st_sem_without_evaluations",
    "Curricular_units_2nd_sem_credited", "Curricular_units_2nd_sem_enrolled",
    "Curricular_units_2nd_sem_evaluations", "Curricular_units_2nd_sem_approved",
    "Curricular_units_2nd_sem_grade", "Curricular_units_2nd_sem_without_evaluations",
    "Unemployment_rate", "Inflation_rate", "GDP"
]


def data_preprocessing(data):
    if not data:  # Checking if the dictionary is empty
        raise ValueError("Input data is empty. Please provide valid data.")
    
    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame([data])  # The data is a dictionary, so wrap it in a list
    
    # Ensure the DataFrame has the same columns as the model was trained on
    df = df[model_columns]  # Reorder columns if necessary

    df = df.apply(pd.to_numeric, errors='coerce') 

    # Check if the DataFrame has the expected columns
    if set(df.columns) != set(model_columns):
        raise ValueError("Input data has incorrect columns. Expected columns: " + str(model_columns))
    
    # Scale the data using the pre-trained scaler
    df_scaled = scaler.transform(df)

    
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    df_scaled = df_scaled.fillna(0) 

    return df_scaled
