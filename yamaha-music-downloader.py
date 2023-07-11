import sys
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# Configure the WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
driver = webdriver.Chrome(
    options=chrome_options)  # Provide the path to the Chrome WebDriver


def download_mp3_files(page_url):
    print(f"Downloading MP3 files from: {page_url}")
    driver.get(page_url)

    # Wait for the desired elements to be present on the page
    wait = WebDriverWait(driver, 10)
    elements = wait.until(
        ec.presence_of_all_elements_located((By.XPATH, "//p[@class='icon']")))
    print(f"Found {len(elements)} elements on the page")

    for element in elements:
        # Extract the name and filename
        name_script = """
            return arguments[0].textContent.trim();
        """
        name = driver.execute_script(name_script, element)
        audio_element = element.find_element(
            By.XPATH,
            "following-sibling::p[@class='audio_play']/div/audio"
        )
        filename = audio_element.get_attribute('src').split('/')[-1]

        print(f"Name: {name}")
        print(f"Filename: {filename}")

        # Download the file and rename it
        download_url = audio_element.get_attribute('src')
        response = requests.get(download_url)
        with open(f"{name}.mp3", 'wb') as file:
            file.write(response.content)
        print(f"Downloaded file: {name}.mp3")

        # Sleep between each download
        time.sleep(1)

    print("Download completed.")


# Check if a URL argument is provided
if len(sys.argv) < 2:
    print("Please provide the URL as the first argument.")
    sys.exit(1)

# Get the URL from the command line argument
url = sys.argv[1]

# Example usage: Pass the URL of the webpage as the first argument
download_mp3_files(url)

# Close the WebDriver
driver.quit()
