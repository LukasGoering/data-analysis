import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import missingno as msno  # Optional: for visualizing missing data
import matplotlib.pyplot as plt
from scipy import stats

## File locations
data_dest = 'data_cleaning_example/clv_data.csv'
save_dest = 'data_cleaning_example/'
save_name = 'clv_data_cleaned.csv'

## (De-)activate print statements
VERBOSE_TEST = False        # Print statements meant for testing and coding
VERBOSE_PROGRAM = True      # Print history of data modifications; Errors are still printed
PLOT = False                # Create plots

def load_data(filepath):
    df = pd.read_csv(filepath)

    # The data set consists of the columns:
    # [unnamed], id, age, gender, income, days_on_platform, city, purchases
    # id is just a continuous index, [unnamed] is identical to the id column

    # Remove the first column with is identical to the second
    df.drop(df.columns[0], axis=1, inplace=True)
    if VERBOSE_PROGRAM:
        print("Removed the first column as duplicate of the seond.")

    return df

### Handle missing values
def handle_missing_data(df):
    ## Analyze missing values
    # Remove columns with more than 30% missing values
    num_samples = len(df)
    for category in df.columns:
        percent_missing = df[category].isna().sum() / num_samples
        if VERBOSE_TEST:
            print(f"Category {category} misses {percent_missing * 100} percent of the data.")
        if percent_missing > 0.3:
            df.drop(category, axis=1, inplace=True)
            if VERBOSE_PROGRAM:
                print(f"Removed category {category} due to {percent_missing*100} percent missing data.")
                
    ## Category "days_on_platform has 2.82% missing data. Impute the values by median.
    if VERBOSE_PROGRAM:
        print(f"Category 'days_on_platform' misses {(df["days_on_platform"].isna().sum() / num_samples) * 100} percent of values.")
    df["days_on_platform"] = df["days_on_platform"].fillna(df["days_on_platform"].median())
    if VERBOSE_PROGRAM:
        print("Missing values for category 'days_on_platform' have been filled by the median value.")

    # Check if all missing values have been filled. Print either a success message or samples with missing values.
    num_rows_with_missing_values = df.isnull().any(axis=1).sum()
    if num_rows_with_missing_values == 0:
        if VERBOSE_PROGRAM:
            print("All missing values have successfully been removed or imputed.")
    else:
        # Print all rows with missing values
        missing_rows = df[df.isnull().any(axis=1)]
        print(f"There are still {num_rows_with_missing_values} samples with missing values.")
        print("Samples with missing values:", missing_rows)

    return df

### Handle outliers
def handle_outliers(df):
    ## Income

    # Calculate absolute Z-score for 'income'
    income_z_score = np.abs(stats.zscore(df["income"]))

    # Count rows before filtering
    original_row_count = len(df)

    # Filter out outliers based on Z-score
    df = df[income_z_score <= 3]

    # Count rows after filtering
    filtered_row_count = len(df)

    # Print number of outliers removed
    if VERBOSE_PROGRAM:
        print(f"Removed {original_row_count - filtered_row_count} outlier(s) based on income Z-score.")

    ## Days on platform: Cap outliers at the 95th quantile
    category = "days_on_platform"

    # Print statistical overview
    if VERBOSE_TEST:
        print("Statistics for 'days_on_platform':")
        print(f"Minimum: {df[category].min():.2f}")
        print(f"Maximum: {df[category].max():.2f}")
        print(f"Mean: {df[category].mean():.2f}")
        print(f"Standard Deviation: {df[category].std():.2f}")

    # Define upper limit, count the values exceeding the limit, cap the values at the upper limit, print the result
    upper_limit = df[category].quantile(0.95)
    num_capped = (df[category] > upper_limit).sum()
    df[category] = np.where(df[category] > upper_limit, upper_limit, df[category])
    if VERBOSE_PROGRAM:
        print(f"{num_capped} value(s) in '{category}' were capped at the 95th percentile ({upper_limit:.2f}).")

    return df

### Scale and normalize data:
def scale_data(df):
    ## Income: Apply log transformation and Standard Scaling
    category = "income"
    df[category] = np.log1p(df[category])  # log1p handles 0 values safely
    scaler = StandardScaler()
    df[category] = scaler.fit_transform(df[[category]])
    if VERBOSE_PROGRAM:
        print(f"Category {category} was log-transformed and scaled to mean zero and standard deviation one.")

    # Rescale: Days on platform and Purchases by Min-Max-Scaling
    for category in ["days_on_platform", "purchases"]:
        scaler = MinMaxScaler()
        df[category] = scaler.fit_transform(df[[category]])
        if VERBOSE_PROGRAM:
            print(f"Category {category} was rescaled by Min-Max-Scaling.")

    return df

### Encode categorical variables
def encode_categorical_data(df):
    # Encode the gender column to 0 for male and 1 for female
    category = "gender"
    df[category] = df[category].map({'Male': 0, 'Female': 1})

    # Check for any invalid values (NaN or values not in [0, 1])
    invalid_values = df[category].isna() | ~df[category].isin([0, 1])

    # Report if any invalid entries are found
    if invalid_values.any():
        print(f"Warning: Invalid or missing values found in {category} column:")
        print(df[invalid_values])
    else:
        if VERBOSE_PROGRAM:
            print(f"Category {category} successfully encoded with only 0 (male) and 1 (female).")

    ## One-Hot Encoding for city-column
    # There are five cities with approximately equal frequencies
    if VERBOSE_TEST:
        # Print the list of cities with their frequency
        city_list = sorted(df['city'].dropna().unique())
        print(df['city'].value_counts())

    # Add "city_" as prefix, create a new column for every city
    df = pd.get_dummies(df, columns=['city'], prefix='city', dtype=int)

    return df

### Save cleaned data
def save_data(df, filepath, filename):
    # Save the cleaned and preprocessed DataFrame to a new CSV file  
    df.to_csv(save_dest + save_name, index=False)
    if VERBOSE_PROGRAM:
        print(f"Data cleaning and preprocessing complete. File saved as {save_name}")

### Preprocess the dataset
df = load_data(data_dest)
df = handle_missing_data(df)
df = handle_outliers(df)
df = encode_categorical_data(df)
save_data(df, save_dest, save_name)