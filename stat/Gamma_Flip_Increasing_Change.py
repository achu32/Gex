import pandas as pd

# Load the CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
data_new = pd.read_csv(file_path)

# Calculate daily percentage change in Close
data_new['Close Change'] = data_new['Close'].pct_change()

# Calculate the differences for Gamma Flip, Call Wall, and Put Wall
gamma_flip_diff_new = data_new['Gamma Flip'].diff()
call_wall_diff_new = data_new['Call Wall'].diff()
put_wall_diff_new = data_new['Put Wall'].diff()

# Define function to calculate statistics for increasing streaks
def calculate_increase_statistics(streak_indices, data):
    # Calculate increases
    increases = [
        data['Close Change'].iloc[i]
        for i in streak_indices if i > 0  # Ensure i > 0 to avoid index errors
    ]

    # Calculate statistics
    total_instances = len(increases)
    num_increases = sum(increase > 0 for increase in increases)
    average_increase = sum(increases) / total_instances if total_instances > 0 else None
    probability_increase = (num_increases / total_instances) * 100 if total_instances > 0 else None

    return average_increase, probability_increase, total_instances, num_increases

# 1. When Gamma Flip increases
streaks_flip_increase = [
    i for i in range(1, len(data_new))  # Start from 1 to ensure valid index for previous day
    if gamma_flip_diff_new.iloc[i] > 0
]
stats_flip_increase = calculate_increase_statistics(streaks_flip_increase, data_new)

# 2. When Gamma Flip increases for three consecutive days
streaks_flip_consecutive_increase = [
    i for i in range(2, len(data_new))  # Start from 2 to check three consecutive days
    if gamma_flip_diff_new.iloc[i] > 0 and gamma_flip_diff_new.iloc[i-1] > 0 and gamma_flip_diff_new.iloc[i-2] > 0
]
stats_flip_consecutive_increase = calculate_increase_statistics(streaks_flip_consecutive_increase, data_new)

# 3. When Gamma Flip and Call Wall both increase
gamma_flip_and_call_wall_increases = (gamma_flip_diff_new > 0) & (call_wall_diff_new > 0)
average_close_change_given_gamma_flip_and_call_wall_increases = (
    data_new['Close Change'][gamma_flip_and_call_wall_increases].mean() * 100
)
total_gamma_flip_and_call_wall_increases = gamma_flip_and_call_wall_increases.sum()
num_close_increases_given_gamma_flip_and_call_wall_increases = data_new['Close Change'][gamma_flip_and_call_wall_increases].gt(0).sum()
probability_close_increases_given_gamma_flip_and_call_wall_increases = (
    num_close_increases_given_gamma_flip_and_call_wall_increases / total_gamma_flip_and_call_wall_increases * 100
)

# 4. When Gamma Flip, Call Wall, and Put Wall all increase
gamma_flip_call_wall_put_wall_increases = (
    (gamma_flip_diff_new > 0) &
    (call_wall_diff_new > 0) &
    (put_wall_diff_new > 0)
)
average_close_change_given_all_increases = (
    data_new['Close Change'][gamma_flip_call_wall_put_wall_increases].mean() * 100
)
total_all_increases = gamma_flip_call_wall_put_wall_increases.sum()
num_close_increases_given_all_increases = data_new['Close Change'][gamma_flip_call_wall_put_wall_increases].gt(0).sum()
probability_close_increases_given_all_increases = (
    num_close_increases_given_all_increases / total_all_increases * 100
) if total_all_increases > 0 else None

# Create a summary table for increases
summary_table_increase = pd.DataFrame({
    "Condition": [
        "Gamma Flip Increases",
        "Gamma Flip Increases for 3 Consecutive Days",
        "Gamma Flip and Call Wall Both Increase",
        "Gamma Flip, Call Wall, and Put Wall All Increase"
    ],
    "Average Increase (%)": [
        stats_flip_increase[0] * 100 if stats_flip_increase[0] is not None else None,
        stats_flip_consecutive_increase[0] * 100 if stats_flip_consecutive_increase[0] is not None else None,
        average_close_change_given_gamma_flip_and_call_wall_increases,
        average_close_change_given_all_increases
    ],
    "Probability of Increase (%)": [
        stats_flip_increase[1],
        stats_flip_consecutive_increase[1],
        probability_close_increases_given_gamma_flip_and_call_wall_increases,
        probability_close_increases_given_all_increases
    ],
    "Total Instances": [
        stats_flip_increase[2],
        stats_flip_consecutive_increase[2],
        total_gamma_flip_and_call_wall_increases,
        total_all_increases
    ],
    "Number of Increases": [
        stats_flip_increase[3],
        stats_flip_consecutive_increase[3],
        num_close_increases_given_gamma_flip_and_call_wall_increases,
        num_close_increases_given_all_increases
    ]
})

# Format the percentage columns
summary_table_increase["Average Increase (%)"] = summary_table_increase["Average Increase (%)"].map("{:.2f}%".format)
summary_table_increase["Probability of Increase (%)"] = summary_table_increase["Probability of Increase (%)"].map("{:.2f}%".format)

import ace_tools as tools; tools.display_dataframe_to_user(name="Summary of Increase Statistics (Percentage Format)", dataframe=summary_table_increase)

summary_table_increase
