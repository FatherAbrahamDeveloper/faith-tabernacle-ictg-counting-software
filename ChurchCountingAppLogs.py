from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import os
import signal
import sys
import atexit

# Function to format duration into hours, minutes, and seconds
def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{hours} hours, {minutes} minutes, and {seconds} seconds"
    elif minutes > 0:
        return f"{minutes} minutes and {seconds} seconds"
    else:
        return f"{seconds} seconds"

# Greet the user
print("Fortune greetings in Jesus' Name and welcome to WWMA Counting App!")

# Request the user to enter the scrape duration
scrape_duration = int(input("Please enter the number of seconds that you want the Counting App to run for: "))

# Request the user to enter the wait time before checking again
wait_time = int(input("Please enter counting interval or the number of seconds to wait before checking again: "))

# Format the scrape duration
formatted_duration = format_duration(scrape_duration)

# Calculate the end time
end_time = datetime.now() + timedelta(seconds=scrape_duration)
formatted_end_time = end_time.strftime('%I:%M:%S %p, %A, %d %B %Y')

# Get the current time
current_time = datetime.now().strftime('%I:%M:%S %p')

# Thank the user and provide the details
print(f"Thanks and God bless you! Your app will run for {formatted_duration} and will be giving updates every {wait_time} seconds.")
print(f"The time is currently {current_time} and this app will stop at {formatted_end_time}.")

# Set up Chrome options
chrome_options = Options()
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

# Variable to hold all report data
all_report_data = ""

# Path to save the accumulated report data with current date and time
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Generate filename with current date and time
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
report_filename = os.path.join(desktop_path, f"WORSHIPPERS_COUNT_{timestamp}.txt")

def save_report():
    """Save the accumulated report data to the file."""
    with open(report_filename, "w") as file:
        file.write(all_report_data)
    print(f"Report successfully saved to {report_filename}")

# Register a cleanup function to be called at exit
atexit.register(save_report)

# Signal handler for graceful exit
def signal_handler(sig, frame):
    print("Interrupt received, saving report...")
    save_report()
    driver.quit()
    sys.exit(0)

# Register signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

try:
    # Wait for the paragraph elements with class name 'information' to be present
    WebDriverWait(driver, 300).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'information'))
    )

    count = 0
    save_interval = 10  # Save every 10 counts

    while (time.time() - start_time) < scrape_duration:
        # Find all paragraph elements with class name 'information'
        information_paragraphs = driver.find_elements(By.CLASS_NAME, 'information')

        # Check if there are at least two elements
        if len(information_paragraphs) >= 2:
            # Get the text from the second element
            second_element_text = information_paragraphs[1].text.split(":")[-1].strip()

            # Get the current date and time
            now = datetime.now().strftime('%I:%M:%S %p, %A, %d %B %Y')

            # Format the message
            message = f"Current Worshippers count as at {now} is: {second_element_text}\n"
            print(message)

            # Append the message to all_report_data
            all_report_data += message

            count += 1

            # Save the accumulated report data to the file every save_interval counts
            if count % save_interval == 0:
                save_report()

        else:
            print("Less than two elements found with the class 'information'.")

        # Wait for the user-defined seconds before checking again
        time.sleep(wait_time)

    # Save the accumulated report data at the end of the run
    save_report()

except Exception as e:
    print(f"Error occurred: {e}")
    # Save the accumulated report data before exiting on error
    save_report()
finally:
    # Save the final accumulated report data to the file
    save_report()
    # Close the driver
    driver.quit()
