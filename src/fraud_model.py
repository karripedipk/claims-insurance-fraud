import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def train_anomaly_model():
    df = pd.read_csv("data/claim_features.csv")

    feature_cols = [
        "claim_amount",
        "shared_device_claim_count",
        "same_provider_claim_count",
        "same_bank_claim_count"
    ]

    X = df[feature_cols].fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42
    )
    df["anomaly_score"] = model.fit_predict(X_scaled)
    df["is_suspicious"] = df["anomaly_score"].apply(lambda x: 1 if x == -1 else 0)

    print(df.sort_values("is_suspicious", ascending=False))
    df.to_csv("data/fraud_predictions.csv", index=False)

if __name__ == "__main__":
    train_anomaly_model()