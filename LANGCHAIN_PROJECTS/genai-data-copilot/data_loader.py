import pandas as pd

def load_csv(file):
    return pd.read_csv(file)

def profile_data(df):
    return {
        "columns": list(df.columns),
        "nulls": df.isnull().sum().to_dict(),
        "stats": df.describe().to_dict()
    }

def get_data_insights(df):
    insights = []

    for col in df.columns:
        if df[col].dtype != "object":
            insights.append(f"{col}: max={df[col].max()}, min={df[col].min()}, avg={df[col].mean()}")

    return "\n".join(insights)