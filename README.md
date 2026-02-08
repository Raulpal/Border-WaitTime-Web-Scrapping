# Border-WaitTime-Web-Scraping

This project contains Python scripts that scrape **historical U.S. border wait time data** from the official U.S. Customs and Border Protection website:

🔗 https://bwt.cbp.gov/historical

The scraped data is processed and saved into **Excel (.xlsx) files** for analysis and reporting.

---

## 📌 What This Project Does

- Uses **Selenium** to interact with the CBP Historical Border Wait Times website
- Selects border **ports, lanes, sub-lanes, and holidays**
- Scrapes the **wait time tables** displayed on the site
- Stores the results in **Excel files**
- Includes scripts to **clean, reformat, and organize** the Excel output for easier use

---

## 📊 Output (Excel Files)

Depending on the script used, the project can generate:

- **Raw Excel files** containing the original CBP table structure
- **Cleaned Excel files** split by holiday
- Excel files with **unnecessary columns removed**
- Sheets ordered by **day of week and time**

Example output files:
- `elpaso_holiday_wait_times.xlsx`
- `elpaso_holiday_wait_times_by_holiday_clean.xlsx`
- `elpaso_holiday_wait_times_by_holiday_clean_sorted.xlsx`

---

## 🧰 Technologies Used

- Python 3
- Selenium WebDriver
- Pandas
- WebDriver Manager
- Excel (openpyxl)

---

## 📂 Project Structure
