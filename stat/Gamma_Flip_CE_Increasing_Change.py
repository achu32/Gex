import pandas as pd

# Load the CSV file
file_path = 'path_to_your_file.csv'
data_new = pd.read_csv(file_path)

# Calculate the differences for Gamma Flip CE, Call Wall CE, and Put Wall CE
gamma_flip_ce_diff_new = data_new['Gamma Flip CE'].diff()
call_wall_ce_diff_new = data_new['Call Wall CE'].diff()
put_wall_ce_diff_new = data_new['Put Wall CE'].diff()

# Define function to calculate statistics for increasing streaks
def calculate_increase_statistics(streak_indices, data):
    # Calculate increases
    increases = [
        (data['Close'].iloc[i+1] - data['Close'].iloc[i]) / data['Close'].iloc[i]
        for i in streak_indices
    ]

    # Calculate statistics
    total_instances = len(increases)
    num_increases = sum(increase > 0 for increase in increases)
    average_increase = sum(increases) / total_instances if total_instances > 0 else None
    probability_increase = (num_increases / total_instances) * 100 if total_instances > 0 else None

    return average_increase, probability_increase, total_instances, num_increases

# 1. When Gamma Flip CE increases
streaks_flip_ce_increase = [
    i for i in range(len(data_new) - 1)
    if gamma_flip_ce_diff_new.iloc[i] > 0
]
stats_flip_ce_increase = calculate_increase_statistics(streaks_flip_ce_increase, data_new)

# 2. When Gamma Flip CE increases for three consecutive days
streaks_flip_ce_consecutive_increase = [
    i for i in range(len(data_new) - 2)
    if gamma_flip_ce_diff_new.iloc[i] > 0 and gamma_flip_ce_diff_new.iloc[i+1] > 0 and gamma_flip_ce_diff_new.iloc[i+2] > 0
]
stats_flip_ce_consecutive_increase = calculate_increase_statistics(streaks_flip_ce_consecutive_increase, data_new)

# 3. When Gamma Flip CE and Call Wall CE both increase
gamma_flip_ce_and_call_wall_ce_increases = (gamma_flip_ce_diff_new > 0) & (call_wall_ce_diff_new > 0)
average_close_change_given_gamma_flip_ce_and_call_wall_ce_increases = (
    data_new['Close'].pct_change()[gamma_flip_ce_and_call_wall_ce_increases].mean() * 100
)
total_gamma_flip_ce_and_call_wall_ce_increases = gamma_flip_ce_and_call_wall_ce_increases.sum()
num_close_increases_given_gamma_flip_ce_and_call_wall_ce_increases = data_new['Close'].diff()[gamma_flip_ce_and_call_wall_ce_increases].gt(0).sum()
probability_close_increases_given_gamma_flip_ce_and_call_wall_ce_increases = (
    num_close_increases_given_gamma_flip_ce_and_call_wall_ce_increases / total_gamma_flip_ce_and_call_wall_ce_increases * 100
)

# 4. When Gamma Flip CE, Call Wall CE, and Put Wall CE all increase
gamma_flip_ce_call_wall_ce_put_wall_ce_increases = (
    (gamma_flip_ce_diff_new > 0) &
    (call_wall_ce_diff_new > 0) &
    (put_wall_ce_diff_new > 0)
)
average_close_change_given_all_increases = (
    data_new['Close'].pct_change()[gamma_flip_ce_call_wall_ce_put_wall_ce_increases].mean() * 100
)
total_all_increases = gamma_flip_ce_call_wall_ce_put_wall_ce_increases.sum()
num_close_increases_given_all_increases = data_new['Close'].diff()[gamma_flip_ce_call_wall_ce_put_wall_ce_increases].gt(0).sum()
probability_close_increases_given_all_increases = (
    num_close_increases_given_all_increases / total_all_increases * 100
) if total_all_increases > 0 else None

# Output the results
print("Gamma Flip CE Increases:", stats_flip_ce_increase)
print("Gamma Flip CE Increases for 3 Consecutive Days:", stats_flip_ce_consecutive_increase)
print("Gamma Flip CE and Call Wall CE Both Increase:", (average_close_change_given_gamma_flip_ce_and_call_wall_ce_increases,
                                                        probability_close_increases_given_gamma_flip_ce_and_call_wall_ce_increases,
                                                        total_gamma_flip_ce_and_call_wall_ce_increases,
                                                        num_close_increases_given_gamma_flip_ce_and_call_wall_ce_increases))
print("Gamma Flip CE, Call Wall CE, and Put Wall CE All Increase:", (average_close_change_given_all_increases,
                                                                     probability_close_increases_given_all_increases,
                                                                     total_all_increases,
                                                                     num_close_increases_given_all_increases))
