import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Filter rows where Open < Gamma Flip
df_open_lt_gamma = df[df['Open'] < df['Gamma Flip']]

# Calculate probabilities for Close, High, Low < Call Wall and Gamma Flip
prob_close_lt_call_wall = (df_open_lt_gamma['Close'] < df_open_lt_gamma['Call Wall']).mean()
prob_high_lt_call_wall = (df_open_lt_gamma['High'] < df_open_lt_gamma['Call Wall']).mean()
prob_low_lt_call_wall = (df_open_lt_gamma['Low'] < df_open_lt_gamma['Call Wall']).mean()

prob_close_lt_gamma_flip = (df_open_lt_gamma['Close'] < df_open_lt_gamma['Gamma Flip']).mean()
prob_high_lt_gamma_flip = (df_open_lt_gamma['High'] < df_open_lt_gamma['Gamma Flip']).mean()
prob_low_lt_gamma_flip = (df_open_lt_gamma['Low'] < df_open_lt_gamma['Gamma Flip']).mean()

# Calculate probabilities for Close, High, Low > Put Wall
prob_close_gt_put_wall = (df_open_lt_gamma['Close'] > df_open_lt_gamma['Put Wall']).mean()
prob_high_gt_put_wall = (df_open_lt_gamma['High'] > df_open_lt_gamma['Put Wall']).mean()
prob_low_gt_put_wall = (df_open_lt_gamma['Low'] > df_open_lt_gamma['Put Wall']).mean()

# Create a DataFrame for the results
probability_df_lt_gamma = pd.DataFrame({
    'Call Wall': [prob_close_lt_call_wall, prob_high_lt_call_wall, prob_low_lt_call_wall],
    'Gamma Flip': [prob_close_lt_gamma_flip, prob_high_lt_gamma_flip, prob_low_lt_gamma_flip],
    'Put Wall': [prob_close_gt_put_wall, prob_high_gt_put_wall, prob_low_gt_put_wall]
}, index=['Close', 'High', 'Low'])

# Convert probabilities to percentages and format
probability_df_lt_gamma_formatted = probability_df_lt_gamma.applymap(lambda x: f"{x * 100:.1f}%")

# Display the probability table
print("Probability Table (Open < Gamma Flip):")
print(probability_df_lt_gamma_formatted)
