import pandas as pd

# Load the CSV file
file_path = 'path_to_your_file.csv'
data_new = pd.read_csv(file_path)

# Calculate the differences for Gamma Flip CE, Call Wall CE, and Put Wall CE
gamma_flip_ce_diff_new = data_new['Gamma Flip CE'].diff()
call_wall_ce_diff_new = data_new['Call Wall CE'].diff()
put_wall_ce_diff_new = data_new['Put Wall CE'].diff()

# Define function to calculate statistics for decreasing streaks
def calculate_decrease_statistics(streak_indices, data):
    # Calculate decreases
    decreases = [
        (data['Close'].iloc[i+1] - data['Close'].iloc[i]) / data['Close'].iloc[i]
        for i in streak_indices
    ]

    # Calculate statistics
    total_instances = len(decreases)
    num_decreases = sum(decrease < 0 for decrease in decreases)
    average_decrease = sum(decreases) / total_instances if total_instances > 0 else None
    probability_decrease = (num_decreases / total_instances) * 100 if total_instances > 0 else None

    return average_decrease, probability_decrease, total_instances, num_decreases

# 1. When Gamma Flip CE decreases
streaks_flip_ce_decrease = [
    i for i in range(len(data_new) - 1)
    if gamma_flip_ce_diff_new.iloc[i] < 0
]
stats_flip_ce_decrease = calculate_decrease_statistics(streaks_flip_ce_decrease, data_new)

# 2. When Gamma Flip CE decreases for three consecutive days
streaks_flip_ce_consecutive_decrease = [
    i for i in range(len(data_new) - 2)
    if gamma_flip_ce_diff_new.iloc[i] < 0 and gamma_flip_ce_diff_new.iloc[i+1] < 0 and gamma_flip_ce_diff_new.iloc[i+2] < 0
]
stats_flip_ce_consecutive_decrease = calculate_decrease_statistics(streaks_flip_ce_consecutive_decrease, data_new)

# 3. When Gamma Flip CE and Put Wall CE both decrease
gamma_flip_ce_and_put_wall_ce_decreases = (gamma_flip_ce_diff_new < 0) & (put_wall_ce_diff_new < 0)
average_close_change_given_gamma_flip_ce_and_put_wall_ce_decreases = (
    data_new['Close'].pct_change()[gamma_flip_ce_and_put_wall_ce_decreases].mean() * 100
)
total_gamma_flip_ce_and_put_wall_ce_decreases = gamma_flip_ce_and_put_wall_ce_decreases.sum()
num_close_decreases_given_gamma_flip_ce_and_put_wall_ce_decreases = data_new['Close'].diff()[gamma_flip_ce_and_put_wall_ce_decreases].lt(0).sum()
probability_close_decreases_given_gamma_flip_ce_and_put_wall_ce_decreases = (
    num_close_decreases_given_gamma_flip_ce_and_put_wall_ce_decreases / total_gamma_flip_ce_and_put_wall_ce_decreases * 100
)

# 4. When Gamma Flip CE, Put Wall CE, and Call Wall CE all decrease
gamma_flip_ce_put_wall_ce_call_wall_ce_decreases = (
    (gamma_flip_ce_diff_new < 0) &
    (put_wall_ce_diff_new < 0) &
    (call_wall_ce_diff_new < 0)
)
average_close_change_given_all_decreases = (
    data_new['Close'].pct_change()[gamma_flip_ce_put_wall_ce_call_wall_ce_decreases].mean() * 100
)
total_all_decreases = gamma_flip_ce_put_wall_ce_call_wall_ce_decreases.sum()
num_close_decreases_given_all_decreases = data_new['Close'].diff()[gamma_flip_ce_put_wall_ce_call_wall_ce_decreases].lt(0).sum()
probability_close_decreases_given_all_decreases = (
    num_close_decreases_given_all_decreases / total_all_decreases * 100
) if total_all_decreases > 0 else None

# Output the results
print("Gamma Flip CE Decreases:", stats_flip_ce_decrease)
print("Gamma Flip CE Decreases for 3 Consecutive Days:", stats_flip_ce_consecutive_decrease)
print("Gamma Flip CE and Put Wall CE Both Decrease:", (average_close_change_given_gamma_flip_ce_and_put_wall_ce_decreases,
                                                        probability_close_decreases_given_gamma_flip_ce_and_put_wall_ce_decreases,
                                                        total_gamma_flip_ce_and_put_wall_ce_decreases,
                                                        num_close_decreases_given_gamma_flip_ce_and_put_wall_ce_decreases))
print("Gamma Flip CE, Put Wall CE, and Call Wall CE All Decrease:", (average_close_change_given_all_decreases,
                                                                     probability_close_decreases_given_all_decreases,
                                                                     total_all_decreases,
                                                                     num_close_decreases_given_all_decreases))
