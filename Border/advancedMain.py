import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Import functions 
from advancedFunction import scrapeCombo

# Where Border average wait time data is
borderURL = "https://bwt.cbp.gov/historical"

# Payloads to inject
# Only need data from ports within El Paso
elPasoPorts =   [
                    "El Paso - Bridge of the Americas (BOTA)",
                    "El Paso - Paso Del Norte (PDN)",
                    "El Paso - Stanton DCL",
                    "El Paso - Ysleta",
                ]

# All Lane Combo
lanes =         [
                    "Commercial",
                    "Passenger",
                    "Pedestrian", 
                ]

# Sublane Combo
sublanes =       [
                    "General",
                    "Nexus/Sentri",
                    "Ready",
                ]


# All months
months =        [
                    "January", "February", "March", "April",
                    "May", "June", "July", "August",
                    "September", "October", "November", "December",
                ]

# Never changes cause easier to get day  data (monday-sunday)
allDays = "All"

# Initialize a headless Chrome browser for scraping JS-rendered pages (need to scrape the Table data)
opts = webdriver.ChromeOptions()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1400,900")

# starts and controls the chrom browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
wait = WebDriverWait(driver, 40)


# Try catch incase exception happens
try:
    # Get All Table Data
    tableData = scrapeCombo(driver, wait, borderURL, elPasoPorts, lanes, sublanes, months, allDays)

    # Store to excel if table has data
    if tableData != None:
        final_df = pd.concat(tableData, ignore_index=True)
        final_df.to_excel("elpaso_border_wait_times.xlsx", index=False)
        print("Saved elpaso_border_wait_times.xlsx")

    else:
        print("No table data")

finally:
    driver.quit()
