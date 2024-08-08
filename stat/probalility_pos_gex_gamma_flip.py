import pandas as pd

# Load the CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Filter rows where Open > Gamma Flip
df_open_gt_gamma = df[df['Open'] > df['Gamma Flip']]

# Calculate probabilities and counts for Close, High, Low < Call Wall
prob_close_lt_call_wall = (df_open_gt_gamma['Close'] < df_open_gt_gamma['Call Wall']).mean()
count_close_lt_call_wall = (df_open_gt_gamma['Close'] < df_open_gt_gamma['Call Wall']).sum()

prob_high_lt_call_wall = (df_open_gt_gamma['High'] < df_open_gt_gamma['Call Wall']).mean()
count_high_lt_call_wall = (df_open_gt_gamma['High'] < df_open_gt_gamma['Call Wall']).sum()

prob_low_lt_call_wall = (df_open_gt_gamma['Low'] < df_open_gt_gamma['Call Wall']).mean()
count_low_lt_call_wall = (df_open_gt_gamma['Low'] < df_open_gt_gamma['Call Wall']).sum()

# Calculate probabilities and counts for Close, High, Low > Gamma Flip and Put Wall
prob_close_gt_gamma_flip = (df_open_gt_gamma['Close'] > df_open_gt_gamma['Gamma Flip']).mean()
count_close_gt_gamma_flip = (df_open_gt_gamma['Close'] > df_open_gt_gamma['Gamma Flip']).sum()

prob_high_gt_gamma_flip = (df_open_gt_gamma['High'] > df_open_gt_gamma['Gamma Flip']).mean()
count_high_gt_gamma_flip = (df_open_gt_gamma['High'] > df_open_gt_gamma['Gamma Flip']).sum()

prob_low_gt_gamma_flip = (df_open_gt_gamma['Low'] > df_open_gt_gamma['Gamma Flip']).mean()
count_low_gt_gamma_flip = (df_open_gt_gamma['Low'] > df_open_gt_gamma['Gamma Flip']).sum()

prob_close_gt_put_wall = (df_open_gt_gamma['Close'] > df_open_gt_gamma['Put Wall']).mean()
count_close_gt_put_wall = (df_open_gt_gamma['Close'] > df_open_gt_gamma['Put Wall']).sum()

prob_high_gt_put_wall = (df_open_gt_gamma['High'] > df_open_gt_gamma['Put Wall']).mean()
count_high_gt_put_wall = (df_open_gt_gamma['High'] > df_open_gt_gamma['Put Wall']).sum()

prob_low_gt_put_wall = (df_open_gt_gamma['Low'] > df_open_gt_gamma['Put Wall']).mean()
count_low_gt_put_wall = (df_open_gt_gamma['Low'] > df_open_gt_gamma['Put Wall']).sum()

# Create a DataFrame for the results (probability and count)
probability_count_df = pd.DataFrame({
    'Call Wall': [(prob_close_lt_call_wall, count_close_lt_call_wall), 
                  (prob_high_lt_call_wall, count_high_lt_call_wall), 
                  (prob_low_lt_call_wall, count_low_lt_call_wall)],
    'Gamma Flip': [(prob_close_gt_gamma_flip, count_close_gt_gamma_flip), 
                   (prob_high_gt_gamma_flip, count_high_gt_gamma_flip), 
                   (prob_low_gt_gamma_flip, count_low_gt_gamma_flip)],
    'Put Wall': [(prob_close_gt_put_wall, count_close_gt_put_wall), 
                 (prob_high_gt_put_wall, count_high_gt_put_wall), 
                 (prob_low_gt_put_wall, count_low_gt_put_wall)]
}, index=['Close', 'High', 'Low'])

# Format probabilities as percentages and include counts
probability_count_df_formatted = probability_count_df.applymap(lambda x: f"({x[0] * 100:.1f}%, {x[1]})")

# Display the probability and count table
print("Probability and Count Table (Open > Gamma Flip):")
print(probability_count_df_formatted)
