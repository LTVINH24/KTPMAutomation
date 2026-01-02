from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 6)

    def click(self, locator):
        attempts = 0
        while attempts < 3:
            try:
                self.wait.until(EC.element_to_be_clickable(locator)).click()
                return 
            except StaleElementReferenceException:
                time.sleep(1)
                attempts += 1
        raise StaleElementReferenceException(f"Không thể click vào {locator} sau 3 lần thử.")

    def send_keys(self, locator, text):
        attempts = 0
        while attempts < 3:
            try:
                elem = self.wait.until(EC.visibility_of_element_located(locator))
                elem.click()
                elem.send_keys(Keys.CONTROL + "a")
                elem.send_keys(Keys.BACKSPACE)
                elem.send_keys(text)
                return 
            except StaleElementReferenceException:
                time.sleep(1)
                attempts += 1
        raise StaleElementReferenceException(f"Không thể nhập liệu vào {locator} sau 3 lần thử.")

    def get_text(self, locator):
        attempts = 0
        while attempts < 3:
            try:
                return self.wait.until(EC.visibility_of_element_located(locator)).text
            except StaleElementReferenceException:
                time.sleep(1)
                attempts += 1
            except:
                return ""
        return ""
            
    def get_toast_message(self):
        try:
            # Toast message hiện nhanh, wait 3s là đủ
            wait = WebDriverWait(self.driver, 3)
            return wait.until(EC.visibility_of_element_located((By.ID, "oxd-toaster_1"))).text
        except:
            return ""