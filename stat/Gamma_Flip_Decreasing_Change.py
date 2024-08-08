import pandas as pd

# Load the uploaded CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
data_new = pd.read_csv(file_path)

# Calculate daily percentage change in Close
data_new['Close Change'] = data_new['Close'].pct_change()

# Calculate the differences for Gamma Flip, Call Wall, and Put Wall
gamma_flip_diff_new = data_new['Gamma Flip'].diff()
call_wall_diff_new = data_new['Call Wall'].diff()
put_wall_diff_new = data_new['Put Wall'].diff()

# Define function to calculate statistics for decreasing streaks
def calculate_decrease_statistics(streak_indices, data):
    # Calculate decreases
    decreases = [
        data['Close Change'].iloc[i]
        for i in streak_indices if i > 0  # Ensure i > 0 to avoid index errors
    ]

    # Calculate statistics
    total_instances = len(decreases)
    num_decreases = sum(decrease < 0 for decrease in decreases)
    average_decrease = sum(decreases) / total_instances if total_instances > 0 else None
    probability_decrease = (num_decreases / total_instances) * 100 if total_instances > 0 else None

    return average_decrease, probability_decrease, total_instances, num_decreases

# 1. When Gamma Flip decreases
streaks_flip_decrease = [
    i for i in range(1, len(data_new))  # Start from 1 to ensure valid index for previous day
    if gamma_flip_diff_new.iloc[i] < 0
]
stats_flip_decrease = calculate_decrease_statistics(streaks_flip_decrease, data_new)

# 2. When Gamma Flip decreases for three consecutive days
streaks_flip_consecutive_decrease = [
    i for i in range(2, len(data_new))  # Start from 2 to check three consecutive days
    if gamma_flip_diff_new.iloc[i] < 0 and gamma_flip_diff_new.iloc[i-1] < 0 and gamma_flip_diff_new.iloc[i-2] < 0
]
stats_flip_consecutive_decrease = calculate_decrease_statistics(streaks_flip_consecutive_decrease, data_new)

# 3. When Gamma Flip and Put Wall both decrease
gamma_flip_and_put_wall_decreases = (gamma_flip_diff_new < 0) & (put_wall_diff_new < 0)
average_close_change_given_gamma_flip_and_put_wall_decreases = (
    data_new['Close Change'][gamma_flip_and_put_wall_decreases].mean() * 100
)
total_gamma_flip_and_put_wall_decreases = gamma_flip_and_put_wall_decreases.sum()
num_close_decreases_given_gamma_flip_and_put_wall_decreases = data_new['Close Change'][gamma_flip_and_put_wall_decreases].lt(0).sum()
probability_close_decreases_given_gamma_flip_and_put_wall_decreases = (
    num_close_decreases_given_gamma_flip_and_put_wall_decreases / total_gamma_flip_and_put_wall_decreases * 100
)

# 4. When Gamma Flip, Put Wall, and Call Wall all decrease
gamma_flip_put_wall_call_wall_decreases = (
    (gamma_flip_diff_new < 0) &
    (put_wall_diff_new < 0) &
    (call_wall_diff_new < 0)
)
average_close_change_given_all_decreases = (
    data_new['Close Change'][gamma_flip_put_wall_call_wall_decreases].mean() * 100
)
total_all_decreases = gamma_flip_put_wall_call_wall_decreases.sum()
num_close_decreases_given_all_decreases = data_new['Close Change'][gamma_flip_put_wall_call_wall_decreases].lt(0).sum()
probability_close_decreases_given_all_decreases = (
    num_close_decreases_given_all_decreases / total_all_decreases * 100
) if total_all_decreases > 0 else None

# Create a summary table
summary_table = pd.DataFrame({
    "Condition": [
        "Gamma Flip Decreases",
        "Gamma Flip Decreases for 3 Consecutive Days",
        "Gamma Flip and Put Wall Both Decrease",
        "Gamma Flip, Put Wall, and Call Wall All Decrease"
    ],
    "Average Decrease (%)": [
        stats_flip_decrease[0] * 100 if stats_flip_decrease[0] is not None else None,
        stats_flip_consecutive_decrease[0] * 100 if stats_flip_consecutive_decrease[0] is not None else None,
        average_close_change_given_gamma_flip_and_put_wall_decreases,
        average_close_change_given_all_decreases
    ],
    "Probability of Decrease (%)": [
        stats_flip_decrease[1],
        stats_flip_consecutive_decrease[1],
        probability_close_decreases_given_gamma_flip_and_put_wall_decreases,
        probability_close_decreases_given_all_decreases
    ],
    "Total Instances": [
        stats_flip_decrease[2],
        stats_flip_consecutive_decrease[2],
        total_gamma_flip_and_put_wall_decreases,
        total_all_decreases
    ],
    "Number of Decreases": [
        stats_flip_decrease[3],
        stats_flip_consecutive_decrease[3],
        num_close_decreases_given_gamma_flip_and_put_wall_decreases,
        num_close_decreases_given_all_decreases
    ]
})

# Format the percentage columns
summary_table["Average Decrease (%)"] = summary_table["Average Decrease (%)"].map("{:.2f}%".format)
summary_table["Probability of Decrease (%)"] = summary_table["Probability of Decrease (%)"].map("{:.2f}%".format)

import ace_tools as tools; tools.display_dataframe_to_user(name="Summary of Gamma Flip, Call Wall, and Put Wall Decrease Statistics (Percentage Format)", dataframe=summary_table)

summary_table
