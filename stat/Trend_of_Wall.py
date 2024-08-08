import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Define the background colors based on the given conditions
colors = []
for _, row in df.iterrows():
    if row['Open'] > row['Gamma Flip']:
        if row['Close'] > row['Call Wall'] or row['Close'] < row['Put Wall']:
            colors.append('orange')  # Orange
        else:
            colors.append('white')
    elif row['Open'] < row['Gamma Flip']:
        if row['Close'] > row['Call Wall'] or row['Close'] < row['Put Wall']:
            colors.append('red')  # Red
        else:
            colors.append('white')
    else:
        colors.append('white')

# Plot the trends for Close, Put Wall, Call Wall, and Gamma Flip with background colors
plt.figure(figsize=(14, 7))

# Plot the lines
plt.plot(df['Date'], df['Close'], label='Close', linewidth=2)
plt.plot(df['Date'], df['Put Wall'], label='Put Wall', linestyle='--')
plt.plot(df['Date'], df['Call Wall'], label='Call Wall', linestyle='-.')
plt.plot(df['Date'], df['Gamma Flip'], label='Gamma Flip', linestyle=':')

# Set background colors
for i, color in enumerate(colors):
    plt.axvspan(df['Date'].iloc[i], df['Date'].iloc[i] + pd.Timedelta(days=1), color=color, alpha=0.3)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('SPX Close, Put Wall, Call Wall, and Gamma Flip Trends with Conditions')
plt.legend()
plt.grid(True)

# Show the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
