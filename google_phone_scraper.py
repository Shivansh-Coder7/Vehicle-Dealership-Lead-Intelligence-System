import argparse
import csv
import random
import re
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None

PHONE_PATTERN = re.compile(r"[+]?\d[\d\s().-]{6,}\d")


def create_driver(headless: bool = False):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1200,900")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    options.add_argument("--lang=en-US,en")

    if ChromeDriverManager is not None:
        service = ChromeService(ChromeDriverManager().install())
    else:
        service = ChromeService()

    return webdriver.Chrome(service=service, options=options)


def normalize_phone(phone_text: str):
    if not phone_text:
        return None
    phone_text = phone_text.strip()
    match = PHONE_PATTERN.search(phone_text)
    if not match:
        return None
    digits = match.group(0)
    normalized = re.sub(r"[()\s.-]+", "", digits)
    return normalized


def extract_phone_from_element(element):
    aria_label = element.get_attribute("aria-label") or ""
    candidate = aria_label.strip() or element.text.strip() or element.get_attribute("href") or ""
    return normalize_phone(candidate)


def find_phone_from_google(driver):
    locators = [
        (By.XPATH, "//*[contains(@aria-label,'Call phone number') or contains(@aria-label,'call phone number')]"),
        (By.XPATH, "//a[contains(@href,'tel:')]"),
        (By.XPATH, "//button[contains(@aria-label,'Call phone number')]"),
        (By.XPATH, "//div[contains(@data-attrid,'phone')]"),
    ]

    for by, locator in locators:
        try:
            elements = driver.find_elements(by, locator)
            for elem in elements:
                phone = extract_phone_from_element(elem)
                if phone:
                    return phone
        except WebDriverException:
            continue

    try:
        body = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        text = body.text
    except TimeoutException:
        text = driver.page_source

    return normalize_phone(text)


def search_and_get_phone(driver, query: str):
    encoded_query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={encoded_query}+phone+number"
    driver.get(url)
    time.sleep(random.uniform(2.5, 4.5))
    phone = find_phone_from_google(driver)
    return phone, url


def read_businesses(csv_path: Path, name_column: str):
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if name_column not in row:
                raise KeyError(f"Column '{name_column}' not found")
            yield row[name_column].strip(), row


def write_results(output_path: Path, rows: list):
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="car_showroom_leads_scored.csv")
    
    parser.add_argument("--output", default="car_showroom_leads_with_phone.csv")
    parser.add_argument("--name-column", default="name")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()

    csv_path = Path(args.input)
    output_path = Path(args.output)

    if not csv_path.exists():
        print(f"Input file not found: {csv_path}")
        return 1

    results = []
    processed = 0
    skipped = 0

    
    try:
        driver = create_driver(headless=args.headless)
    except Exception as e:
        print(f"Failed to start browser: {e}")
        return 2

    try:
        for index, (name, original_row) in enumerate(read_businesses(csv_path, args.name_column)):
            if index < args.start:
                skipped += 1
                continue
            if args.limit and processed >= args.limit:
                break
            if not name:
                continue

            print(f"[{index+1}] Searching phone for: {name}")

            try:
                
                try:
                    _ = driver.title
                except Exception:
                    print("  Browser crashed, restarting...")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    driver = create_driver(headless=args.headless)

                phone, search_url = search_and_get_phone(driver, name)
                status = "found" if phone else "not found"
                print(f"  Phone: {phone or 'not found'}")

            except Exception as e:
                phone = None
                status = f"error: {e}"
                search_url = ""
                print(f"  Error: {e}")

                
                try:
                    driver.quit()
                except Exception:
                    pass
                try:
                    driver = create_driver(headless=args.headless)
                except Exception:
                    pass

            row = dict(original_row)
            row["google_search_url"] = search_url
            row["extracted_phone"] = phone or ""
            row["scrape_status"] = status
            results.append(row)
            processed += 1

            
            if processed % 5 == 0:
                write_results(output_path, results)
                print(f"  Progress saved ({processed} done so far)")

            time.sleep(random.uniform(3.0, 5.0))

    finally:
        try:
            driver.quit()
        except Exception:
            pass

    write_results(output_path, results)
    print(f"\nDone! Processed {processed}, skipped {skipped}")
    print(f"Results saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())