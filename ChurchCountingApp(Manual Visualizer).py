import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Extract timestamps and values from your data
timestamps = [datetime.strptime(t, '%I:%M %p') for t in [
    '6:06 AM',
    '6:13 AM',
    '6:32 AM',
    '6:43 AM',
    '7:01 AM',
    '7:14 AM',
    '7:30 AM',
    '7:48 AM',
    '8:10 AM',
    '8:18 AM',
    '8:29 AM',
    '8:58 AM',
    '9:08 AM',
    '9:22 AM',
    '9:38 AM',
    '9:49 AM',
    '10:09 AM',
    '10:46 AM',
    '11:02 AM',
    '11:31 AM'
]]
values = [
    67,
    398,
    970,
    1224,
    1795,
    2141,
    2510,
    2877,
    3331,
    3544,
    3758,
    4205,
    4519,
    4893,
    5193,
    5356,
    5636,
    5912,
    6214,
    5463
]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(timestamps, values, marker='o', linestyle='-', color='r')

# Annotate each point with its value
for i, (timestamp, value) in enumerate(zip(timestamps, values)):
    plt.annotate(str(value), (timestamp, value), textcoords="offset points", xytext=(0, 10), ha='right', fontsize=7)

# Format x-axis to show dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%I:%M:%S %p'))  # Include seconds and AM/PM
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))  # Set major ticks at 10-minute intervals
plt.gcf().autofmt_xdate()

# Add title and labels
plt.title('SERVICE TITLE: INSERT SERVICE TITLE HERE', fontweight='bold', pad=20)
plt.xlabel('TIME', fontweight='bold')
plt.ylabel('WORSHIPPERS COUNT', fontweight='bold')

ax = plt.gca()  # Get the current axis
ax.spines['top'].set_visible(False)  # Hide top border
ax.spines['right'].set_visible(False)  # Hide right border

# Show the plot
plt.show()
