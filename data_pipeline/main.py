import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import missingno as msno  # Optional: for visualizing missing data
import matplotlib.pyplot as plt
from scipy import stats

# Print statements
VERBOSE = False

# File destinations
load_path = 'data_pipeline/data_dummy.csv'
save_path = 'data_pipeline/data_cleaned.csv'

## Step 0: Generate and load the dummy data
# Create a dummy dataset
def generate_data(load_path):
    np.random.seed(0)
    dummy_data = {
        'Feature1': np.random.normal(100, 10, 100).tolist() + [np.nan, 200],  # Normally distributed with an outlier
        'Feature2': np.random.randint(0, 100, 102).tolist(),  # Random integers
        'Category': ['A', 'B', 'C', 'D'] * 25 + [np.nan, 'A'],  # Categorical with some missing values
        'Target': np.random.choice([0, 1], 102).tolist()  # Binary target variable
    }

    # Convert the dictionary to a pandas DataFrame
    df_dummy = pd.DataFrame(dummy_data)
    save_data(df_dummy, load_path)


## Step 1: Define the preprocessing tools
def load_data(filepath):
    return pd.read_csv(filepath)

def handle_missing_values(df):
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].mean())    # For numeric data, fill missing values with the mean
    return df

def remove_outliers(df):
    z_scores = np.abs(stats.zscore(df.select_dtypes(include=[np.number])))
    return df[(z_scores < 3).all(axis=1)].copy()  # Remove rows with any outliers

def scale_data(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    df[numeric_cols] = pd.DataFrame(
    scaler.fit_transform(df[numeric_cols].astype(float)),
    columns=numeric_cols,
    index=df.index
    )
    return df

def encode_categorical(df, categorical_columns):
    df.loc[:, categorical_columns] = df[categorical_columns].fillna('Unknown')
    return pd.get_dummies(df, columns=categorical_columns)

def save_data(df, output_filepath):
    df.to_csv(output_filepath, index=False)

## Step 2: Apply data processing tools to the data set
# Generate the data
generate_data(load_path)

# Load the data
df_preprocessed = load_data(load_path)

# Handle missing values
df_preprocessed = handle_missing_values(df_preprocessed)
# Remove outliers
df_preprocessed = remove_outliers(df_preprocessed)

# Scale the data
df_preprocessed = scale_data(df_preprocessed)

# Encode categorical variables
df_preprocessed = encode_categorical(df_preprocessed, ['Category'])

# Display the preprocessed data
if VERBOSE:
    print(df_preprocessed.head())

# Save the cleaned and preprocessed DataFrame to a CSV file
save_data(df_preprocessed, save_path)

## Step 3: Evaluation
if VERBOSE:
    # Check for missing values:
    print(df_preprocessed.isnull().sum())
    # Verify outlier removal:
    print(df_preprocessed.describe())
    # Inspect scaled data:
    print(df_preprocessed.head())
    # Check categorical encoding:
    print(df_preprocessed.columns)
# Print success message
print(f'Preprocessing complete. Preprocessed data saved as {save_path}')
