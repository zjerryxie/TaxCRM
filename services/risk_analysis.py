# app/services/risk_analysis.py
from datetime import datetime
from app.models import Client

def check_deadlines(client: Client) -> bool:
    deadlines = { '1040': datetime(client.tax_year, 4, 15) }
    return datetime.now() > deadlines.get(client.form_type)

# app/services/risk_analysis.py
from sklearn.ensemble import RandomForestClassifier

#def audit_risk_score(client: Client) -> float:
#    model = load_model()  # Pre-trained
#    return model.predict([[client.income, client.deductions]])

from joblib import load
import os

# Load pre-trained model (or train in __init__)
model = load(os.path.join(os.path.dirname(__file__), 'model.pkl')) 

def audit_risk_score(client: Client) -> float:
    features = [[client.income, client.deductions]]  # Customize based on model
    return model.predict_proba(features)[0][1]

from dateutil.parser import parse

def predict_deadline(client: Client) -> dict:
    """Dynamic deadline prediction considering extensions, state rules"""
    base_deadline = datetime(client.tax_year, 4, 15)
    if client.state == "CA":
        base_deadline += timedelta(days=6)  # CA extensions
    
    return {
        "standard": base_deadline,
        "extension": base_deadline + timedelta(days=180)
    }

from sklearn.metrics import classification_report

def evaluate_model(X_test, y_test):
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))  # Log precision/recall
    mlflow.log_metrics(classification_report(y_test, y_pred, output_dict=True))
