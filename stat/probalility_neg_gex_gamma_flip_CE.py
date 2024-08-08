import pandas as pd

# Load the CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Filter rows where Open < Gamma Flip CE
df_open_lt_gamma_ce = df[df['Open'] < df['Gamma Flip CE']]

# Calculate probabilities and counts for Close, High, Low < Call Wall CE and Gamma Flip CE
prob_close_lt_call_wall_ce = (df_open_lt_gamma_ce['Close'] < df_open_lt_gamma_ce['Call Wall CE']).mean()
count_close_lt_call_wall_ce = (df_open_lt_gamma_ce['Close'] < df_open_lt_gamma_ce['Call Wall CE']).sum()

prob_high_lt_call_wall_ce = (df_open_lt_gamma_ce['High'] < df_open_lt_gamma_ce['Call Wall CE']).mean()
count_high_lt_call_wall_ce = (df_open_lt_gamma_ce['High'] < df_open_lt_gamma_ce['Call Wall CE']).sum()

prob_low_lt_call_wall_ce = (df_open_lt_gamma_ce['Low'] < df_open_lt_gamma_ce['Call Wall CE']).mean()
count_low_lt_call_wall_ce = (df_open_lt_gamma_ce['Low'] < df_open_lt_gamma_ce['Call Wall CE']).sum()

prob_close_lt_gamma_flip_ce = (df_open_lt_gamma_ce['Close'] < df_open_lt_gamma_ce['Gamma Flip CE']).mean()
count_close_lt_gamma_flip_ce = (df_open_lt_gamma_ce['Close'] < df_open_lt_gamma_ce['Gamma Flip CE']).sum()

prob_high_lt_gamma_flip_ce = (df_open_lt_gamma_ce['High'] < df_open_lt_gamma_ce['Gamma Flip CE']).mean()
count_high_lt_gamma_flip_ce = (df_open_lt_gamma_ce['High'] < df_open_lt_gamma_ce['Gamma Flip CE']).sum()

prob_low_lt_gamma_flip_ce = (df_open_lt_gamma_ce['Low'] < df_open_lt_gamma_ce['Gamma Flip CE']).mean()
count_low_lt_gamma_flip_ce = (df_open_lt_gamma_ce['Low'] < df_open_lt_gamma_ce['Gamma Flip CE']).sum()

# Calculate probabilities and counts for Close, High, Low > Put Wall CE
prob_close_gt_put_wall_ce = (df_open_lt_gamma_ce['Close'] > df_open_lt_gamma_ce['Put Wall CE']).mean()
count_close_gt_put_wall_ce = (df_open_lt_gamma_ce['Close'] > df_open_lt_gamma_ce['Put Wall CE']).sum()

prob_high_gt_put_wall_ce = (df_open_lt_gamma_ce['High'] > df_open_lt_gamma_ce['Put Wall CE']).mean()
count_high_gt_put_wall_ce = (df_open_lt_gamma_ce['High'] > df_open_lt_gamma_ce['Put Wall CE']).sum()

prob_low_gt_put_wall_ce = (df_open_lt_gamma_ce['Low'] > df_open_lt_gamma_ce['Put Wall CE']).mean()
count_low_gt_put_wall_ce = (df_open_lt_gamma_ce['Low'] > df_open_lt_gamma_ce['Put Wall CE']).sum()

# Create a DataFrame for the results (probability and count)
probability_count_df_ce = pd.DataFrame({
    'Call Wall CE': [(prob_close_lt_call_wall_ce, count_close_lt_call_wall_ce), 
                     (prob_high_lt_call_wall_ce, count_high_lt_call_wall_ce), 
                     (prob_low_lt_call_wall_ce, count_low_lt_call_wall_ce)],
    'Gamma Flip CE': [(prob_close_lt_gamma_flip_ce, count_close_lt_gamma_flip_ce), 
                      (prob_high_lt_gamma_flip_ce, count_high_lt_gamma_flip_ce), 
                      (prob_low_lt_gamma_flip_ce, count_low_lt_gamma_flip_ce)],
    'Put Wall CE': [(prob_close_gt_put_wall_ce, count_close_gt_put_wall_ce), 
                    (prob_high_gt_put_wall_ce, count_high_gt_put_wall_ce), 
                    (prob_low_gt_put_wall_ce, count_low_gt_put_wall_ce)]
}, index=['Close', 'High', 'Low'])

# Format probabilities as percentages and include counts
probability_count_df_ce_formatted = probability_count_df_ce.applymap(lambda x: f"({x[0] * 100:.1f}%, {x[1]})")

# Display the probability and count table
import ace_tools as tools; tools.display_dataframe_to_user(name="Probability and Count Table (Open < Gamma Flip CE)", dataframe=probability_count_df_ce_formatted)

probability_count_df_ce_formatted
