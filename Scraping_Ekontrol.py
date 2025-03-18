from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

# Set up the Selenium WebDriver for Microsoft Edge
driver = webdriver.Edge()  # Make sure you have the Edge WebDriver installed
driver.get('https://ekontrol.pl/pl/33570/scheme/g422p06')

# Wait for you to log in (adjust the time as needed)
input("Press Enter after logging in...")

# Wait for the page to load completely
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Get the page source
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all <g> elements with class 'ReadField'
    read_field_elements = soup.find_all('g', class_='ReadField')

    # Unicode representation of '°C'
    temperature_pattern = re.compile(r'\d+\s*[\u00B0C]')  # Handles possible spaces

    matches = []
    for elem in read_field_elements:
        text_elements = elem.find_all('text')
        for text_elem in text_elements:
            match = temperature_pattern.search(text_elem.text)
            if match:
                matches.append(match.group().strip())

    # Assign each value to a variable dynamically
    variables = {}
    for i, value in enumerate(matches):
        variables[f"T{i+1}"] = value

    if variables:
        for key, value in variables.items():
            print(f"{key} = {value}")  # Print each variable and its value
    else:
        print('No match found')

    print(f"Found {len(matches)} temperature values")
except Exception as e:
    print(f"Error: {e}")

driver.quit()