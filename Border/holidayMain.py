import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from holidayFunction import scrapeComboHoliday


# Payloads to inject
# Only need data from ports within El Paso
elPasoPorts = [
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
sublanes =      [
                    "General",
                    "Nexus/Sentri",
                    "Ready",
                ]


# Holidays to select
holidays = [
    "New Years Day",
    "Martin Luther King Jr. Day",
    "Presidents Day",
    "Memorial Day",
    "Independence Day",
    "Labor Day",
    "Columbus Day",
    "Veterans Day",
    "Thanksgiving Day",
    "Christmas Day",
]


def main():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    wait = WebDriverWait(driver, 40)

    try:
        url = "https://bwt.cbp.gov/historical"

        tables = scrapeComboHoliday(
            driver=driver,
            wait=wait,
            url=url,
            ports=elPasoPorts,
            lanes=lanes,
            sublanes=sublanes,
            holidays=holidays,
        )

        if tables:
            final_df = pd.concat(tables, ignore_index=True)
            output_file = "elpaso_holiday_wait_times.xlsx"
            final_df.to_excel(output_file, index=False)
            print(f"Saved {len(final_df)} rows to {output_file}")
        else:
            print("No valid tables scraped (tables list is empty).")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()