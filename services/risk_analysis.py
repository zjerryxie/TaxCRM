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
