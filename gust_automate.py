from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os


def get_geckodriver_path():
    current_directory = os.path.dirname(__file__)
    return os.path.join(current_directory, "geckodriver.exe")


def initialize_driver(geckodriver_path):
    gecko_service = Service(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=gecko_service)
    return driver


def login(driver, email, password):
    driver.get("https://gust.com/users/sign_in")
    driver.find_element(By.ID, "user_email").send_keys(email)
    driver.find_element(By.NAME, "user[password]").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "#sign_in").click()


def access_notifications(driver):
    driver.get("https://gust.com/alerts")
    pass


def main():
    geckodriver_path = get_geckodriver_path()
    driver = initialize_driver(geckodriver_path)

    email = "email"
    password = "password"

    login(driver, email, password)

    base_url = "https://gust.com/search/new?category=startups"
    wait = WebDriverWait(driver, 5)

    for page_number in range(1, 29910):
        page_url = f"{base_url}&page={page_number}&partial=results"
        driver.get(page_url)

        container = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='search_results_list' and @class='results']")))
        list_items = container.find_elements(By.XPATH, ".//li[@class='list-group-item']")

        for item in list_items:
            company_link = item.find_element(By.XPATH, ".//a[contains(@href, '/companies/')]")
            company_url = company_link.get_attribute("href")
            company_name = company_link.text
            print(f"Visiting company: {company_name}")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(company_url)

            pitch_deck_link = driver.find_element(By.XPATH, "//a[contains(@href, 'pitch_deck')]")

            if pitch_deck_link:
                pitch_deck_url = pitch_deck_link.get_attribute("href")
                driver.get(pitch_deck_url)
                time.sleep(3)

            try:
                request_button = driver.find_element(By.XPATH,
                                                     "//a[@id='request_more_info' and @class='btn btn-primary']")
                request_button.click()

                text_box = driver.find_element(By.ID, "information_request_personal_message")
                text_box.send_keys("Message to send to companies")
                time.sleep(3)
                # send_button = driver.find_element(By.XPATH, "//input[@name='commit' and @value='Send ']")
                # send_button.click()

            except NoSuchElementException:
                print("No request access button found")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':
    main()
