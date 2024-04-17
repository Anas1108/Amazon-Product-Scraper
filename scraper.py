from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import time
from datetime import datetime

PRODUCT_LIMIT = 1
REVIEWS_LIMIT = 1

class Scraper:
    def __init__(self):
        try:
            options = Options()
            options.headless = True
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Firefox(options=options)
        except Exception as e:
            print("Error occurred while initializing webdriver:", e)

        self.base_url = 'https://www.amazon.com/s'

    def fetch_product_data(self, product_name):
        try:
            driver = self.driver
            driver.get(self.base_url)

            search_box = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
            search_box.clear()
            search_box.send_keys(product_name)
            search_box.send_keys(Keys.RETURN)

            time.sleep(2)

            all_links = self.extract_product_links(driver)
            all_links = all_links[:PRODUCT_LIMIT]

            product_data = {}

            for link in all_links:
                product_info = {}

                Product_Title = self.extract_product_Title(driver, link)
                print("Extracting Title:", Product_Title)

                Product_Price = self.extract_product_Price(driver, link)
                print("Extracting Price:", Product_Price)

                Product_Img_URL = self.extract_product_Img_URL(driver, link)
                print("Extracting Image URL:", Product_Img_URL)

                Product_Reviews = self.extract_product_reviews(driver, link, limit=REVIEWS_LIMIT)
                print("Extracting Reviews:", Product_Reviews)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                product_info["price"] = Product_Price
                product_info["image_url"] = Product_Img_URL
                product_info["reviews"] = Product_Reviews
                product_info["timestamp"] = timestamp

                product_data[Product_Title] = product_info

            return product_data
        except Exception as e:
            print("Error occurred during scraping:", e)
            return {}

    def extract_product_links(self, driver):
        try:
            h2_elements = driver.find_elements(By.XPATH, '//h2[contains(@class, "a-size-mini")]')
            all_links = []

            for h2_element in h2_elements:
                a_tag = h2_element.find_element(By.XPATH, './/a')
                link = a_tag.get_attribute("href")
                all_links.append(link)

            return all_links
        except Exception as e:
            print("Error occurred while extracting product links:", e)
            return []

    def extract_product_Title(self, driver, link):
        try:
            driver.get(link)
            Title = driver.find_element(By.XPATH, '//h1[contains(@class, "a-size-large a-spacing-none")]').text
            return Title
        except Exception as e:
            print("Error occurred while extracting product title:", e)
            return ""

    def extract_product_Price(self, driver, link):
        try:
            price_element = driver.find_element(By.ID, "desktop_buybox")
            price = price_element.text
            pattern = r'^\$\d+(\.\d+)?\b'
            match = re.search(pattern, price, re.MULTILINE)

            if match:
                price = match.group(0)
                return price
            else:
                return "Out Of Stock"
        except Exception as e:
            print("Error occurred while extracting product price:", e)
            return ""

    def extract_product_Img_URL(self, driver, link):
        try:
            img_element = driver.find_element(By.ID, "landingImage")
            image_link = img_element.get_attribute("src")
            return image_link
        except Exception as e:
            print("Error occurred while extracting product image URL:", e)
            return ""

    def extract_product_reviews(self, driver, link, limit=1):
        try:
            a_element = driver.find_element(By.CLASS_NAME, "a-link-emphasis.a-text-bold")
            url = a_element.get_attribute("href")
            driver.get(url)
            Reviews = []
            for i in range(limit):
                div_elements = driver.find_elements(By.CLASS_NAME, "a-section.review.aok-relative")
                for div_element in div_elements:
                    Reviews.append(div_element.text.strip())

                try:
                    li_element = driver.find_element(By.CLASS_NAME, "a-last")
                    a_tag = li_element.find_element(By.TAG_NAME, "a")
                    href_link = a_tag.get_attribute("href")
                    driver.get(href_link)
                except:
                    break
            return Reviews
        except Exception as e:
            print("Error occurred while extracting product reviews:", e)
            return []

    def QuitDriver(self):
        try:
            self.driver.quit()
        except Exception as e:
            print("Error occurred while quitting driver:", e)
