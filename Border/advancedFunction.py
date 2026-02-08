import pandas as pd
from io import StringIO

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


# Helper Function (Selctore for dropdown options)
def selector(wait, css, text):
    el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
    Select(el).select_by_visible_text(text)


# Helper Function (Clickable objects (Calculate, Table tab))
def clickable(wait, xpath):
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


# Helper Function (Get Table data
def scrapeTable(wait, driver):
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class,'cbpStriped')]//td[normalize-space()='Midnight']")))
    table_el = driver.find_element(By.XPATH, "//table[contains(@class,'cbpStriped')]")
    html = table_el.get_attribute("outerHTML")

    return pd.read_html(StringIO(html))[0]

# Function to go through all combinations.
# Will store all table  data for all valid combo
def scrapeCombo(driver,wait,url,ports,lanes,sublanes,months,day):

    # Store All Table Data
    allTables = []
    # Go to Border wait time URL page
    driver.get(url)

    # Gor through difference combinations
    for port in ports:
        for lane in lanes:
            for sublane in sublanes:
                for month in months:
                    # Try catch incase exeption happens
                    try:

                        # Fill The dropdown boxes
                        selector(wait, "select#port", port)
                        selector(wait, "select#lane", lane)
                        selector(wait, "select#sublane", sublane)
                        selector(wait, "select#month", month)
                        selector(wait, "select#day", day)

                        # Click Calculate button and Table tab
                        clickable(wait, "//button[contains(.,'Calculate')]")
                        clickable(wait, "//a[normalize-space()='Table']")

                        # Get Table data
                        df = scrapeTable(wait, driver)

                        # Add columns so each row keeps the selected port, lane, sublane, month, and day
                        df.insert(0, "Port", port)
                        df.insert(1, "Lane", lane)
                        df.insert(2, "Sub-Lane", sublane)
                        df.insert(3, "Month", month)
                        df.insert(4, "Day", day)

                        # Add to list
                        allTables.append(df)

                    except Exception as e:
                        # Table combo invalid so dont add
                        print("Invalid Combo")

    # Return All the Table data
    return allTables

