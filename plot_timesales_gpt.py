import matplotlib.pyplot as plt

# Your DataFrame
df = quotes.get_timesales('KO', start_time='2023-09-01')

# Extract the 'time' and 'close' columns
time_series = df['time']
close_prices = df['close']

# Convert the 'time' column to a datetime object
time_series = pd.to_datetime(time_series)

# Create the time series plot
plt.figure(figsize=(12, 6))
plt.plot(time_series, close_prices, label='Close Price', color='blue')
plt.title('Time Series Plot of Close Prices')
plt.xlabel('Time')
plt.ylabel('Close Price')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
