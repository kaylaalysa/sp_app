import joblib

model = joblib.load("model/rf_model.joblib")


def prediction(data):
    result = model.predict(data)
    
    label_mapping = {0: "Dropout", 1: "Enrolled", 2: "Graduate"}
    
    final_result = [label_mapping[label] for label in result]
    
    return final_result
