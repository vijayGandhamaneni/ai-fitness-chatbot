import pandas as pd


# Load raw dataset

df = pd.read_csv("data/fitness_dataset.csv")


# Display original dataset info

print("\nOriginal Dataset Shape:")
print(df.shape)


# -------------------------------
# DATA PREPROCESSING
# -------------------------------


# Step 1: Remove duplicate rows

df = df.drop_duplicates()


# Step 2: Convert all text to lowercase

df["condition"] = (
    df["condition"]
    .str.lower()
)

df["exercise"] = (
    df["exercise"]
    .str.lower()
)

df["precaution"] = (
    df["precaution"]
    .str.lower()
)
df["goal"] =(
    df["goal"]
    .str.lower()
)
df["difficulty"] =(
    df["difficulty"]
    .str.lower()
)
df["steps"] =(
    df["steps"]
    .str.lower()
)


# Step 3: Remove extra spaces

df["condition"] = (
    df["condition"]
    .str.strip()
)

df["exercise"] = (
    df["exercise"]
    .str.strip()
)

df["precaution"] = (
    df["precaution"]
    .str.strip()
)
df["goal"] =(
    df["goal"]
    .str.strip()
)
df["difficulty"] =(
    df["difficulty"]
    .str.strip()
)
df["steps"] =(
    df["steps"]
    .str.strip()
)

# Step 4: Remove missing values

df = df.dropna()


# Step 5: Reset index

df = df.reset_index(drop=True)


# Display cleaned dataset info

print("\nCleaned Dataset Shape:")
print(df.shape)


# Preview cleaned dataset

print("\nCleaned Dataset Preview:")
print(df.head())


# Save cleaned dataset

df.to_csv(
    "data/cleaned_fitness_data.csv",
    index=False
)


print("\nPreprocessing Completed Successfully!")
print("Cleaned dataset saved as cleaned_fitness_dataset.csv")