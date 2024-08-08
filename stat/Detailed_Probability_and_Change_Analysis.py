# Execute the complete modified code and display full results

import pandas as pd
from itertools import product

# Load the CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
data = pd.read_csv(file_path)

# Step 1: Calculate daily changes for Call Wall CE, Put Wall CE, and Gamma Flip CE
data['Call Wall CE Change'] = data['Call Wall CE'].diff()
data['Put Wall CE Change'] = data['Put Wall CE'].diff()
data['Gamma Flip CE Change'] = data['Gamma Flip CE'].diff()

# Calculate percentage changes
data['Call Wall CE Change %'] = data['Call Wall CE Change'] / data['Call Wall CE'].shift(1) * 100
data['Put Wall CE Change %'] = data['Put Wall CE Change'] / data['Put Wall CE'].shift(1) * 100
data['Gamma Flip CE Change %'] = data['Gamma Flip CE Change'] / data['Gamma Flip CE'].shift(1) * 100

# Step 2: Determine the increase or decrease
data['Call Wall CE Direction'] = data['Call Wall CE Change'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')
data['Put Wall CE Direction'] = data['Put Wall CE Change'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')
data['Gamma Flip CE Direction'] = data['Gamma Flip CE Change'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')

# Step 3: Calculate the percentage change in closing price to determine up or down
data['Close Change'] = data['Close'].pct_change()
data['Close Direction'] = data['Close Change'].apply(lambda x: 'Up' if x > 0 else 'Down')

# Step 4: Determine when all indicators decrease simultaneously
data['All Decrease'] = (data['Call Wall CE Change'] < 0) & (data['Put Wall CE Change'] < 0) & (data['Gamma Flip CE Change'] < 0)

# Generate all possible combinations of changes
combinations = list(product(['Increase', 'Decrease'], repeat=3))
combination_results_with_total = []

# Step 5: Calculate probabilities and average percentage change for each combination with total count
for call_change, put_change, gamma_change in combinations:
    if call_change == 'Decrease' and put_change == 'Decrease' and gamma_change == 'Decrease':
        subset = data[data['All Decrease']]
    else:
        subset = data[
            (data['Call Wall CE Direction'] == call_change) &
            (data['Put Wall CE Direction'] == put_change) &
            (data['Gamma Flip CE Direction'] == gamma_change)
        ]

    up_count = subset[subset['Close Direction'] == 'Up'].shape[0]
    down_count = subset[subset['Close Direction'] == 'Down'].shape[0]
    total_count = subset.shape[0]

    if total_count > 0:
        up_probability = (up_count / total_count) * 100
        down_probability = (down_count / total_count) * 100

        avg_call_change_percent = subset['Call Wall CE Change %'].mean()
        avg_put_change_percent = subset['Put Wall CE Change %'].mean()
        avg_gamma_change_percent = subset['Gamma Flip CE Change %'].mean()
    else:
        up_probability = down_probability = None
        avg_call_change_percent = avg_put_change_percent = avg_gamma_change_percent = None

    combination_results_with_total.append({
        'Call Wall CE': f"{call_change} ({avg_call_change_percent:.2f}%)" if avg_call_change_percent else f"{call_change} (-)",
        'Put Wall CE': f"{put_change} ({avg_put_change_percent:.2f}%)" if avg_put_change_percent else f"{put_change} (-)",
        'Gamma Flip CE': f"{gamma_change} ({avg_gamma_change_percent:.2f}%)" if avg_gamma_change_percent else f"{gamma_change} (-)",
        'Up Probability %': f"{up_probability:.2f} ({up_count}/{total_count})" if up_probability and up_probability >= 50 else '-',
        'Down Probability %': f"{down_probability:.2f} ({down_count}/{total_count})" if down_probability and down_probability >= 50 else '-',
    })

# Step 6: Convert the results into a DataFrame and display
results_df_with_total = pd.DataFrame(combination_results_with_total)

# Display the detailed results with total count
import ace_tools as tools; tools.display_dataframe_to_user(name="Probability and Change Analysis with Total Count", dataframe=results_df_with_total)

results_df_with_total.head(10)
