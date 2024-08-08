import pandas as pd

# Load the CSV file
file_path = 'path_to_your_file.csv'
data_new = pd.read_csv(file_path)

# Calculate the differences for Gamma Flip and Put Wall
gamma_flip_diff_new = data_new['Gamma Flip'].diff()
put_wall_diff_new = data_new['Put Wall'].diff()

# Define function to calculate statistics for decreasing streaks
def calculate_decline_statistics(streak_indices, data):
    # Calculate declines
    declines = [
        (data['Close'].iloc[i+1] - data['Close'].iloc[i]) / data['Close'].iloc[i]
        for i in streak_indices
    ]

    # Calculate statistics
    total_instances = len(declines)
    num_decreases = sum(decline < 0 for decline in declines)
    average_decline = sum(declines) / total_instances if total_instances > 0 else None
    probability_decline = (num_decreases / total_instances) * 100 if total_instances > 0 else None

    return average_decline, probability_decline, total_instances, num_decreases

# 1. When Gamma Flip decreases
streaks_flip_decrease = [
    i for i in range(len(data_new) - 1)
    if gamma_flip_diff_new.iloc[i] < 0
]
stats_flip_decrease = calculate_decline_statistics(streaks_flip_decrease, data_new)

# 2. When Gamma Flip decreases for three consecutive days
streaks_flip_consecutive_decrease = [
    i for i in range(len(data_new) - 2)
    if gamma_flip_diff_new.iloc[i] < 0 and gamma_flip_diff_new.iloc[i+1] < 0 and gamma_flip_diff_new.iloc[i+2] < 0
]
stats_flip_consecutive_decrease = calculate_decline_statistics(streaks_flip_consecutive_decrease, data_new)

# 3. When Gamma Flip and Put Wall both decrease
gamma_flip_and_put_wall_decreases = (gamma_flip_diff_new < 0) & (put_wall_diff_new < 0)
average_close_change_given_gamma_flip_and_put_wall_decreases = (
    data_new['Close'].pct_change()[gamma_flip_and_put_wall_decreases].mean() * 100
)
total_gamma_flip_and_put_wall_decreases = gamma_flip_and_put_wall_decreases.sum()
num_close_decreases_given_gamma_flip_and_put_wall_decreases = data_new['Close'].diff()[gamma_flip_and_put_wall_decreases].lt(0).sum()
probability_close_decreases_given_gamma_flip_and_put_wall_decreases = (
    num_close_decreases_given_gamma_flip_and_put_wall_decreases / total_gamma_flip_and_put_wall_decreases * 100
)

# Output the results
print("Gamma Flip Decreases:", stats_flip_decrease)
print("Gamma Flip Decreases for 3 Consecutive Days:", stats_flip_consecutive_decrease)
print("Gamma Flip and Put Wall Both Decrease:", (average_close_change_given_gamma_flip_and_put_wall_decreases,
                                                  probability_close_decreases_given_gamma_flip_and_put_wall_decreases,
                                                  total_gamma_flip_and_put_wall_decreases,
                                                  num_close_decreases_given_gamma_flip_and_put_wall_decreases))
