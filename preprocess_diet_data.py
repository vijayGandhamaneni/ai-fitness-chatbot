import pandas as pd

# Load raw dataset
df = pd.read_csv("data/diet_data.csv")

# Remove duplicates
df = df.drop_duplicates()

# Remove null values
df = df.dropna()

# Convert text columns to lowercase
columns = [
    "goal",
    "condition",
    "diet_type",
    "foods",
    "avoid",
    "hydration",
    "meal_tip"
]

for col in columns:

    df[col] = df[col].str.lower()

# Save cleaned dataset
df.to_csv(
    "data/cleaned_diet_data.csv",
    index=False
)

print("Cleaned diet dataset created successfully!")