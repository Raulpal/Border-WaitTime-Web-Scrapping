import pandas as pd
from io import StringIO

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


TABLES_XPATH = "//table[contains(@class,'cbpStriped')]"

def select_visible(driver, wait, css, text):
    """Select by visible text from the *visible* copy of a duplicated <select>."""
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css)))
    els = driver.find_elements(By.CSS_SELECTOR, css)
    visible = next((el for el in els if el.is_displayed()), None)
    if visible is None:
        raise NoSuchElementException(f"No visible element found for {css}")

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", visible)
    Select(visible).select_by_visible_text(text)


def click_visible_xpath(driver, wait, xpath):
    """Click the *visible+enabled* copy of a duplicated element matched by XPath."""
    wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    els = driver.find_elements(By.XPATH, xpath)
    visible = next((el for el in els if el.is_displayed() and el.is_enabled()), None)
    if visible is None:
        raise NoSuchElementException(f"No visible+enabled element found for XPath: {xpath}")

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", visible)
    driver.execute_script("arguments[0].click();", visible)


def scrapeTable_visible(wait, driver):
    """Read the visible cbpStriped table using pandas.read_html (same style as Advanced)."""
    wait.until(EC.presence_of_element_located((By.XPATH, TABLES_XPATH)))

    tables = driver.find_elements(By.XPATH, TABLES_XPATH)
    table_el = next((t for t in tables if t.is_displayed()), None)
    if table_el is None:
        raise NoSuchElementException("No visible cbpStriped table found")

    # Wait until populated
    wait.until(lambda d: "Midnight" in (table_el.text or ""))

    html = table_el.get_attribute("outerHTML")
    return pd.read_html(StringIO(html))[0]


def scrapeComboHoliday(driver, wait, url, ports, lanes, sublanes, holidays):
    """
    Loop through combinations on /historical Holiday tab.
    Returns list of DataFrames (like your Advanced version).
    """
    allTables = []
    driver.get(url)

    # Make sure we're on Holiday tab once
    click_visible_xpath(driver, wait, "//a[normalize-space()='Holiday']")

    for port in ports:
        for lane in lanes:
            for sublane in sublanes:
                for holiday in holidays:
                    try:
                        # IMPORTANT: /historical uses sholiday
                        select_visible(driver, wait, "select#port", port)
                        select_visible(driver, wait, "select#lane", lane)
                        select_visible(driver, wait, "select#sublane", sublane)
                        select_visible(driver, wait, "select#sholiday", holiday)

                        click_visible_xpath(driver, wait, "//button[contains(.,'Calculate')]")
                        click_visible_xpath(driver, wait, "//a[normalize-space()='Table']")

                        df = scrapeTable_visible(wait, driver)

                        df.insert(0, "Port", port)
                        df.insert(1, "Lane", lane)
                        df.insert(2, "Sub-Lane", sublane)
                        df.insert(3, "Holiday", holiday)

                        allTables.append(df)

                    except Exception as e:
                        print(f"Invalid/failed combo: {(port, lane, sublane, holiday)} | {type(e).__name__}")

    return allTables