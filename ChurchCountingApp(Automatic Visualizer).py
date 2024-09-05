from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import os
import matplotlib.pyplot as plt


def format_time(seconds):
    """Convert seconds into hours, minutes, and seconds as needed."""
    if seconds >= 3600:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours} hour(s), {minutes} minute(s), and {secs} second(s)"
    elif seconds >= 60:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes} minute(s) and {secs} second(s)"
    else:
        return f"{seconds} second(s)"


# Display a greeting
print("Fortune greetings and welcome to our WWMA Counting App plotter/visualizer")

# Request user inputs
scrape_duration_seconds = int(
    input("Kindly enter how long (in seconds) you want the app to run for: "))
interval_duration_seconds = int(
    input("Kindly enter the interval (in seconds) to wait before checking again (please note that this will determine the number of plotted points): "))

# Convert and format the durations
formatted_scrape_duration = format_time(scrape_duration_seconds)
formatted_interval_duration = format_time(interval_duration_seconds)

# Thank the user and provide a message
print(
    f"Thank you! Your app will run for {formatted_scrape_duration} and will be giving updates every {formatted_interval_duration}.")

# Get the current time and calculate the end time
current_time = datetime.now()
end_time = current_time + timedelta(seconds=scrape_duration_seconds)

# Format the current time and end time
formatted_current_time = current_time.strftime('%I:%M:%S %p')
formatted_end_time = end_time.strftime('%I:%M:%S %p')

# Display the friendly message
print(
    f"The current time is {formatted_current_time} and this app will terminate at {formatted_end_time}.")

# Set up Chrome options
chrome_options = Options()
# Run in headless mode (no browser UI)
chrome_options.add_argument("--headless")

# Path to the manually downloaded ChromeDriver
chrome_driver_path = r'C:\Users\Developer\Desktop\The New Man\Church Counting Software\ChromeDriver\chromedriver.exe'

# Set up Chrome driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://ictgapi-bpog-git-dev-aina-oluwatimilehins-projects.vercel.app/LiveService"

# Open the URL
driver.get(url)

start_time = time.time()  # Record the start time

# Variables to hold the data for plotting
timestamps = []
counts = []

try:
    # Wait for the paragraph elements with class name 'information' to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'information'))
    )

    while (time.time() - start_time) < scrape_duration_seconds:
        # Find all paragraph elements with class name 'information'
        information_paragraphs = driver.find_elements(
            By.CLASS_NAME, 'information')

        # Check if there are at least two elements
        if len(information_paragraphs) >= 2:
            # Get the text from the second element
            second_element_text = information_paragraphs[1].text

            # Extract the count from the text
            try:
                count = int(second_element_text.split(":")[-1].strip())
            except ValueError:
                count = 0

            # Get the current time
            current_time = datetime.now().strftime('%I:%M:%S %p')
            timestamps.append(current_time)
            counts.append(count)

            # Print the message
            message = f"Current Worshippers count as at {current_time} is: {count}"
            print(message)
        else:
            print("Less than two elements found with the class 'information'.")

        time.sleep(interval_duration_seconds)  # Wait before checking again

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, counts, marker='o', linestyle='-', color='r')

    # Annotate each data point with the count
    for i, txt in enumerate(counts):
        plt.annotate(txt, (timestamps[i], counts[i]), textcoords="offset points", xytext=(
            0, 10), ha='center', fontsize=8)

    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Timestamp', fontweight='bold')
    plt.ylabel('Online Worshippers Count', fontweight='bold')
    plt.title(information_paragraphs[0].text, pad=50, fontweight='bold')
    plt.tight_layout()
    ax = plt.gca()  # Get the current axis
    ax.spines['top'].set_visible(False)  # Hide top border
    ax.spines['right'].set_visible(False)  # Hide right border

    # Generate filename based on current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    plot_filename = os.path.join(
        desktop_path, f"WorshippersCount_{current_datetime}.jpg")
    plt.savefig(plot_filename)

    # Verify if the file is saved
    if os.path.exists(plot_filename):
        print(f"Plot successfully saved to {plot_filename}")
    else:
        print(f"Failed to save the plot to {plot_filename}")

except Exception as e:
    print(f"Error occurred: {e}")
finally:
    # Close the driver
    driver.quit()
    plt.close()  # Close the plot
