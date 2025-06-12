import pandas as pd
import os

# Set the path for the original raw dataset and the cleaned output file
input_path = os.path.join("..", "data", "raw", "StudentsPerformance.csv")
output_path = os.path.join("..", "data", "processed", "clean_students.csv")

# Load the dataset using pandas
df = pd.read_csv(input_path)

# Clean the column names by removing spaces and making all letters lowercase
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Add a new column called 'average_score' which is the mean of math, reading, and writing scores
df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1)

# Convert all categorical columns into numerical format using one-hot encoding
# drop_first=True helps to avoid multicollinearity by removing the first category from each feature
df_encoded = pd.get_dummies(df, drop_first=True)

# Make sure the output folder exists (if not, it will create it)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the cleaned and encoded data to a CSV file
df_encoded.to_csv(output_path, index=False)

# Print success message to confirm it worked
print("✅ Preprocessing complete. Cleaned data saved to:", output_path)
