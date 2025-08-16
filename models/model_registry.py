import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

def log_model(model, name: str):
    mlflow.sklearn.log_model(model, name)
    mlflow.log_metric("accuracy", model.score(X_test, y_test))
