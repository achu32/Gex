# Trend of Gamma Flip, Open and Close Prices
import pandas as pd
import matplotlib.pyplot as plt

# Re-load the data and apply the new plotting style
data = pd.read_csv(new_file_path)

# Convert 'Date' column to string format for plotting
data['Date'] = data['Date'].astype(str)

# Plot the trend of Gamma Flip CE, Open, and Close prices with specified background color conditions
plt.figure(figsize=(14, 8))

# Plot with background colors based on conditions
for i in range(len(data)):
    if data['Open'][i] > data['Gamma Flip CE'][i] and data['Close'][i] < data['Gamma Flip CE'][i]:
        plt.axvspan(i - 0.5, i + 0.5, color='orange', alpha=0.3)
    elif data['Open'][i] > data['Gamma Flip CE'][i]:
        plt.axvspan(i - 0.5, i + 0.5, color='lightgreen', alpha=0.3)
    elif data['Open'][i] < data['Gamma Flip CE'][i] and data['Close'][i] > data['Gamma Flip CE'][i]:
        plt.axvspan(i - 0.5, i + 0.5, color='darkgreen', alpha=0.3)
    else:
        plt.axvspan(i - 0.5, i + 0.5, color='lightcoral', alpha=0.3)

# Plot lines
plt.plot(data['Date'], data['Gamma Flip CE'], marker='o', linestyle='-', color='g', label='Gamma Flip CE')
plt.plot(data['Date'], data['Open'], marker='o', linestyle='-', color='b', label='Open')
plt.plot(data['Date'], data['Close'], marker='o', linestyle='-', color='r', label='Close')

# Add titles and labels
plt.title('Trend of Gamma Flip CE, Open, and Close Prices')
plt.xlabel('Date')
plt.ylabel('Price')

# Adjust x-ticks to avoid overlap
plt.xticks(ticks=range(0, len(data), max(1, len(data) // 15)), labels=data['Date'][::max(1, len(data) // 15)], rotation=45)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()

