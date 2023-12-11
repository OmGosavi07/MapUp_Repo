import pandas as pd

def generate_car_matrix():
    # Load the dataset-1.csv into a DataFrame
    df = pd.read_csv("/Users/omgosavi/Downloads/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv")

    # Create a pivot table using id_1 as index, id_2 as columns, and car as values
    result_df = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0
    result_df = result_df.fillna(0)

    # Set diagonal values to 0
    for col in result_df.columns:
        result_df.at[col, col] = 0

    return result_df

# Call the function
result_dataframe = generate_car_matrix()

# Print the result
print(result_dataframe)


def get_type_count(df: pd.DataFrame) -> dict:
    """
    Categorizes 'car' values into types, calculates the count of occurrences for each car_type category,
    and returns the result as a dictionary. The dictionary is sorted alphabetically based on keys.

    Args:
        df (pandas.DataFrame): Input DataFrame with 'car' column.

    Returns:
        dict: A dictionary with car types as keys and their counts as values, sorted alphabetically.
    """
    # Add a new column 'car_type' based on the specified conditions
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

# Example usage:
# Assuming df is your DataFrame from dataset-1.csv
# df = pd.read_csv("dataset-1.csv")
# result = get_type_count(df)
# print(result)



def get_bus_indexes(df: pd.DataFrame) -> list:
    """
    Identifies indices where the 'bus' values are greater than twice the mean value of the 'bus' column.

    Args:
        df (pandas.DataFrame): Input DataFrame with 'bus' column.

    Returns:
        list: List of indices where 'bus' values exceed twice the mean, sorted in ascending order.
    """

    #import dataset-2
    # Filter rows where 'car' is 'bus'
    bus_rows = df[df['car'] == 'bus']

    # Calculate the mean of the 'bus' column
    bus_mean = bus_rows['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = bus_rows.index[bus_rows['bus'] > 2 * bus_mean].tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Example usage:
# Assuming df is your DataFrame from dataset-1.csv
# df = pd.read_csv("dataset-1.csv")
# result = get_bus_indexes(df)
# print(result)


def filter_routes(df: pd.DataFrame) -> list:
    """
    Filters and returns a sorted list of route values for which the average 'truck' values are greater than 7.

    Args:
        df (pandas.DataFrame): Input DataFrame with 'route' and 'truck' columns.

    Returns:
        list: Sorted list of route values with average 'truck' values greater than 7.
    """
    # Group by 'route' and calculate the mean of 'truck' values
    average_truck_values = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' values are greater than 7
    filtered_routes = average_truck_values[average_truck_values > 7].index.tolist()

    # Sort the list of routes
    filtered_routes.sort()

    return filtered_routes

# Example usage:
# Assuming df is your DataFrame from dataset-1.csv
# df = pd.read_csv("dataset-1.csv")
# result = filter_routes(df)
# print(result)


def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Multiplies matrix values based on custom conditions.

    Args:
        matrix (pandas.DataFrame): Input matrix DataFrame.

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Apply custom conditions to modify values
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Example usage:
# Assuming result_dataframe is the DataFrame from Question 1
# result_dataframe = generate_car_matrix(df)
# modified_result = multiply_matrix(result_dataframe)
# print(modified_result)


def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Verifies the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair
    cover a full 24-hour period and span all 7 days of the week.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns id, id_2, and timestamp.

    Returns:
        pd.Series: Boolean series indicating if each (id, id_2) pair has incorrect timestamps. Multi-index is (id, id_2).
    """

    # Load the dataset-2.csv into a DataFrame
    df = pd.read_csv("/Users/omgosavi/Downloads/MapUp-Data-Assessment-F-main/datasets/dataset-2.csv")

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Extract day of the week and hour of the day
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['hour_of_day'] = df['timestamp'].dt.hour

    # Create a mask for incorrect timestamps
    incorrect_timestamp_mask = (
        (df['day_of_week'].isin(range(7))) &  # Check if day of the week is valid (0 to 6, Monday to Sunday)
        (df['hour_of_day'].isin(range(24)))   # Check if hour of the day is valid (0 to 23)
    )

    # Group by (id, id_2) and check if all timestamps are correct for each group
    result_series = df.groupby(['id', 'id_2'])['timestamp'].apply(lambda x: incorrect_timestamp_mask.loc[x.index].all())

    return result_series

# Example usage:
# Assuming df is your DataFrame from dataset-2.csv
# df = pd.read_csv("dataset-2.csv")
# result = time_check(df)
# print(result)
