import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = '/mnt/data/GEX-Stat - SPX-fixed.csv'
data = pd.read_csv(file_path)

# Calculate percentage change for Gamma Flip and Close
data['Gamma Flip Change'] = data['Gamma Flip'].pct_change() * 100
data['Close Change'] = data['Close'].pct_change() * 100

# Define the range and increment
range_start = -2.0
range_end = 2.5
increment = 0.5

# Create a list to store results
gamma_flip_close_changes = []

# Calculate average changes for each range
current_start = range_start
while current_start < range_end:
    current_end = current_start + increment
    # Filter the Gamma Flip changes within the current range
    current_range_changes = data['Gamma Flip Change'][
        (data['Gamma Flip Change'] >= current_start) & (data['Gamma Flip Change'] < current_end)
    ]
    # Get the corresponding Close changes
    corresponding_close_changes = data['Close Change'].iloc[current_range_changes.index]
    # Calculate averages
    average_gamma_flip_change = current_range_changes.mean()
    average_close_change = corresponding_close_changes.mean()
    count = len(current_range_changes)
    # Append results to the list
    gamma_flip_close_changes.append((f"{current_start}% to {current_end}%", average_gamma_flip_change, average_close_change, count))
    # Increment the range
    current_start += increment

# Convert results to DataFrame for plotting
gamma_flip_close_changes_df = pd.DataFrame(gamma_flip_close_changes, columns=['Gamma Flip Change Range', 'Average Gamma Flip Change', 'Average Close Change', 'Count'])

# Plot the results
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot Data Counts as a light gray bar chart
ax1.bar(gamma_flip_close_changes_df['Gamma Flip Change Range'], gamma_flip_close_changes_df['Count'], color='lightgray', alpha=0.7, label='Count of Data Points', width=0.4)

# Add labels and title for the bar chart
ax1.set_xlabel('Gamma Flip Change Range (%)')
ax1.set_ylabel('Count of Data Points', color='gray')
ax1.set_title('Average Close Change and Count of Data Points')
ax1.tick_params(axis='y', labelcolor='gray')
ax1.set_xticks(range(len(gamma_flip_close_changes_df['Gamma Flip Change Range'])))
ax1.set_xticklabels(gamma_flip_close_changes_df['Gamma Flip Change Range'], rotation=45)
ax1.legend(loc='upper left')

# Secondary axis for the trend line showing Close Changes
ax2 = ax1.twinx()
ax2.plot(gamma_flip_close_changes_df['Gamma Flip Change Range'], gamma_flip_close_changes_df['Average Close Change'], 'o-', color='green', label='Close Change (%)', markersize=8)
ax2.set_ylabel('Average Close Change (%)', color='green')
ax2.tick_params(axis='y', labelcolor='green')
ax2.set_ylim(-2, 2)

# Annotate close changes on the trend line
for i, txt in enumerate(gamma_flip_close_changes_df['Average Close Change']):
    color = 'green' if txt > 0 else 'red'
    ax2.annotate(f"{txt:.2f}%", (i, gamma_flip_close_changes_df['Average Close Change'][i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=9, color=color)

fig.tight_layout()
plt.show()
