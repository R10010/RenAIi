"""
Train churn prediction model using TU Wien Telco dataset
Covers experiments: model training, evaluation, MLflow tracking
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
import mlflow
import mlflow.sklearn
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    df = pd.read_csv("data/raw/churn/telco_churn.csv")
    # Preprocessing: encode categorical variables, handle missing
    df = df.dropna()
    # Convert target to binary
    df["Churn"] = (df["Churn"] == "Yes").astype(int)
    # Select features (simplified)
    features = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    ]
    X = pd.get_dummies(df[features], drop_first=True)
    y = df["Churn"]
    return X, y


def train():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run(run_name="churn_prediction"):
        model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_params({"n_estimators": 100, "max_depth": 10})
        mlflow.log_metrics(
            {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}
        )

        # Log confusion matrix plot
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Confusion Matrix")
        plt.savefig("confusion_matrix.png")
        mlflow.log_artifact("confusion_matrix.png")

        # Log feature importance
        importance = pd.DataFrame(
            {"feature": X.columns, "importance": model.feature_importances_}
        ).sort_values("importance", ascending=False)
        importance.to_csv("feature_importance.csv", index=False)
        mlflow.log_artifact("feature_importance.csv")

        mlflow.sklearn.log_model(model, "churn_model")

        # Register model
        mlflow.register_model(
            f"runs:/{mlflow.active_run().info.run_id}/churn_model", "ChurnModel"
        )

        # Save locally
        joblib.dump(model, "ml_pipeline/models/churn/model.pkl")

        print(f"Accuracy: {acc:.3f}, F1: {f1:.3f}")


if __name__ == "__main__":
    train()
