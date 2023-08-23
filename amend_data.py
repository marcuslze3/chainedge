import datetime


def convert_time_ago_to_datetime(time_str, reference_datetime):
    """Convert a string like 'X mins ago' or 'Y hrs, X mins ago' to a datetime object."""
    
    # Split the string by space to get individual components
    parts = time_str.split()
    
    # Determine the time difference based on the string format
    if "min" in time_str and "hr" not in time_str:
        minutes_ago = int(parts[0])
        time_delta = datetime.timedelta(minutes=minutes_ago)
    elif "hr" in time_str and "min" not in time_str:
        hours_ago = int(parts[0])
        time_delta = datetime.timedelta(hours=hours_ago)
    elif "hr" in time_str and "min" in time_str:
        hours_ago = int(parts[0])
        minutes_ago = int(parts[2])
        time_delta = datetime.timedelta(hours=hours_ago, minutes=minutes_ago)
    else:
        return None
    
    # Subtract the time difference from the reference time to get the actual datetime
    actual_datetime = reference_datetime - time_delta
    return actual_datetime

# Define the reference time as provided
reference_time = datetime.datetime(2023, 8, 23, 14, 27)

import pandas as pd

df = pd.read_csv('data.csv')

# Convert the 'tn_time' column
df['tn_time'] = df['tn_time'].apply(lambda x: convert_time_ago_to_datetime(x, reference_time))

df.to_csv('new_data.csv')

# Display the first few rows with the new datetime column
df[['tn_time']].head()