import pandas as pd

import networkx as nx

def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the distance matrix between toll locations based on known routes.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'start_toll', 'end_toll', and 'distance'.

    Returns:
        pd.DataFrame: Distance matrix with cumulative distances along known routes. Diagonal values are set to 0.
    """

    df = pd.read_csv("/Users/omgosavi/Downloads/MapUp-Data-Assessment-F-main/datasets/dataset-3.csv")
    # Create a directed graph
    G = nx.Graph()

    # Add edges with distances to the graph
    for _, row in df.iterrows():
        G.add_edge(row['start_toll'], row['end_toll'], distance=row['distance'])
        G.add_edge(row['end_toll'], row['start_toll'], distance=row['distance'])  # Bidirectional edge

    # Calculate all pairs shortest paths
    all_pairs_shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G))

    # Create a DataFrame for the distance matrix
    toll_ids = sorted(set(df['start_toll'].unique()) | set(df['end_toll'].unique()))
    distance_matrix = pd.DataFrame(index=toll_ids, columns=toll_ids)

    # Fill the distance matrix with cumulative distances along known routes
    for start_toll in toll_ids:
        for end_toll in toll_ids:
            distance_matrix.at[start_toll, end_toll] = all_pairs_shortest_paths[start_toll].get(end_toll, 0)

    # Set diagonal values to 0
    distance_matrix.values[[range(len(toll_ids))]*2] = 0

    return distance_matrix

# Example usage:
# Assuming df is your DataFrame from dataset-3.csv
# result = calculate_distance_matrix(df)
# print(result)



def unroll_distance_matrix(distance_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame with columns 'id_start', 'id_end', and 'distance'.

    Args:
        distance_matrix (pandas.DataFrame): Input DataFrame representing the distance matrix.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Create a list to store the unrolled data
    unrolled_data = []

    # Iterate through the rows of the distance matrix
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            # Skip same 'id_start' and 'id_end'
            if id_start != id_end:
                # Append the data to the unrolled list
                unrolled_data.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance_matrix.at[id_start, id_end]
                })

    # Create a DataFrame from the unrolled data
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

# Example usage:
# Assuming result is the DataFrame from Question 1
# result = calculate_distance_matrix(df)
# unrolled_result = unroll_distance_matrix(result)
# print(unrolled_result)

def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_id: int) -> list:
    """
    Find all IDs from the 'id_start' column whose average distance is within 10% of the reference value's average.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_start', 'id_end', and 'distance'.
        reference_id (int): Reference value from the 'id_start' column.

    Returns:
        list: Sorted list of 'id_start' values within 10% of the reference value's average distance.
    """
    # Filter DataFrame for the reference_id
    reference_data = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_average_distance = reference_data['distance'].mean()

    # Calculate the lower and upper bounds for the threshold (10%)
    lower_bound = reference_average_distance * 0.9
    upper_bound = reference_average_distance * 1.1

    # Filter 'id_start' values within the threshold
    filtered_ids = df[(df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]['id_start']

    # Remove duplicates and sort the result
    sorted_filtered_ids = sorted(set(filtered_ids))

    return sorted_filtered_ids

# Example usage:
# Assuming unrolled_result is the DataFrame from Question 2
# reference_id = 123


def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the input DataFrame.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_start', 'id_end', 'distance'.

    Returns:
        pandas.DataFrame: DataFrame with additional columns 'moto', 'car', 'rv', 'bus', and 'truck' representing toll rates.
    """
    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

# Example usage:
# Assuming unrolled_result is the DataFrame from Question 2
# toll_rates_result = calculate_toll_rate(unrolled_result)
# print(toll_rates_result)


def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_start', 'id_end', 'distance', and toll rates for each vehicle type.

    Returns:
        pandas.DataFrame: DataFrame with additional columns 'start_day', 'start_time', 'end_day', 'end_time', and 'discounted_rate'.
    """
    # Define time ranges and discount factors
    time_ranges_weekdays = [(time(0, 0, 0), time(10, 0, 0)),
                            (time(10, 0, 0), time(18, 0, 0)),
                            (time(18, 0, 0), time(23, 59, 59))]
    
    time_ranges_weekends = [(time(0, 0, 0), time(23, 59, 59))]

    discount_factors_weekdays = [0.8, 1.2, 0.8]
    discount_factor_weekends = 0.7

    # Create empty lists to store the calculated data
    start_days, start_times, end_days, end_times, discounted_rates = [], [], [], [], []

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        # Iterate through time ranges based on weekdays or weekends
        for time_range, discount_factor in zip(time_ranges_weekdays, discount_factors_weekdays) if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else time_ranges_weekends:
            start_time, end_time = time_range

            # Calculate start and end datetime objects for the current time range
            start_datetime = datetime.combine(datetime.today(), start_time)
            end_datetime = datetime.combine(datetime.today(), end_time)

            # Check if the row's start_time falls within the current time range
            if start_datetime <= row['start_time'] <= end_datetime:
                # Apply the discount factor to the vehicle columns
                discounted_rates.append(row[['moto', 'car', 'rv', 'bus', 'truck']] * discount_factor)

                # Append the start and end day, start and end time to the lists
                start_days.append(row['start_day'])
                end_days.append(row['end_day'])
                start_times.append(start_time)
                end_times.append(end_time)
                break  # Move to the next row after finding the matching time range

    # Create a DataFrame from the calculated data
    result_df = pd.DataFrame({
        'start_day': start_days,
        'start_time': start_times,
        'end_day': end_days,
        'end_time': end_times,
        'discounted_rate': discounted_rates
    })

    # Concatenate the original DataFrame with the calculated DataFrame
    result_df = pd.concat([df, result_df], axis=1)

    return result_df

# Example usage:
# Assuming toll_rates_result is the DataFrame from Question 4
# time_based_toll_rates_result = calculate_time_based_toll_rates(toll_rates_result)
# print(time_based_toll_rates_result)
