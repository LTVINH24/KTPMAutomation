from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import time
from selenium.webdriver.support.ui import WebDriverWait
class TimePage(BasePage):
    # --- LOCATORS ---
    BTN_EDIT = (By.XPATH, "//button[text()=' Edit ']")
    BTN_SUBMIT = (By.XPATH, "//button[text()=' Submit ']")
    BTN_APPROVE = (By.XPATH, "//button[text()=' Approve ']")
    BTN_REJECT = (By.XPATH, "//button[text()=' Reject ']")
    BTN_SAVE = (By.XPATH, "//button[@type='submit']")

    STATUS_LABEL = (By.XPATH, "//p[@class='oxd-text oxd-text--p oxd-text--subtitle-2']") 

    INPUT_PROJECT = (By.XPATH, "//input[@placeholder='Type for hints...']")
    DROPDOWN_ACTIVITY = (By.XPATH, "//div[contains(@class, 'oxd-select-text--active')]")
    INPUT_TIME = (By.XPATH, "//td[contains(@class, 'duration-input')]//input")
    BTN_COMMENT = (By.XPATH, "//button[contains(@class, 'orangehrm-timesheet-icon-comment')]")
    TEXTAREA_COMMENT = (By.XPATH, "//textarea[@placeholder='Comment here']")
    BTN_SAVE_COMMENT = (By.XPATH, "//div[contains(@class, 'oxd-dialog-sheet')]//button[contains(., 'Save')]")

    ERROR_MESSAGE = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")
    ERROR_MESSAGE_COMMENT = (By.XPATH, "//textarea[@placeholder='Comment here']/ancestor::div[contains(@class, 'oxd-input-group')]//span[contains(@class, 'oxd-input-field-error-message')]")
    BTN_CANCEL_COMMENT = (By.XPATH, "//div[contains(@class, 'oxd-dialog-sheet')]//button[contains(., 'Cancel')]")
    def __init__(self, driver):
        super().__init__(driver)
        self.captured_error_message = ""
    def navigate_my_timesheet(self):
        self.driver.get("http://localhost:8080/web/index.php/time/viewMyTimesheet")
        try:
            WebDriverWait(self.driver, 5).until(
                EC.any_of(
                    EC.visibility_of_element_located(self.BTN_EDIT),
                    EC.visibility_of_element_located(self.BTN_SAVE)
                )
            )
        except: pass
    def create_timesheet_entry(self, project, activity, time_val, comment=None):
        self.captured_error_message = ""
        
        self.click(self.BTN_EDIT)
        try:
            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.BTN_SAVE))
        except TimeoutException:
            # Fallback: Nếu mạng lag click chưa ăn, click lại lần nữa
            self.click(self.BTN_EDIT)
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.BTN_SAVE))
        if project:
            try:
                self.send_keys(self.INPUT_PROJECT, project)
                time.sleep(1) 
                try:
                    self.driver.find_element(By.XPATH, "//div[@role='option'][1]").click()
                except:
                    self.driver.find_element(*self.INPUT_PROJECT).send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Lỗi Project: {e}")
        
        if activity:
            try:
                self.click(self.DROPDOWN_ACTIVITY)
                time.sleep(0.5)
                try:
                    self.driver.find_element(By.XPATH, f"//div[@role='option']//span[text()='{activity}']").click()
                except:
                    self.click((By.XPATH, "//div[@role='option'][2]"))
            except Exception as e:
                print(f"Lỗi Activity: {e}")
        
        if time_val:   
            self.send_keys(self.INPUT_TIME, time_val)
            try:
                short_wait = WebDriverWait(self.driver, 0.5)
                error_elem = short_wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
                if error_elem.is_displayed():
                    self.captured_error_message = error_elem.text
                    print(f"-> [LOG] Đã bắt được lỗi Time ngay khi nhập: '{self.captured_error_message}'")
            except TimeoutException:
                pass 

        if comment and project and activity and not self.captured_error_message:
            short_wait = WebDriverWait(self.driver, 0.5)
            try:
                btn_cmt = short_wait.until(EC.visibility_of_element_located(self.BTN_COMMENT))
                btn_cmt.click()
                
                short_wait.until(EC.visibility_of_element_located(self.TEXTAREA_COMMENT))
                self.send_keys(self.TEXTAREA_COMMENT, comment)
                self.click(self.BTN_SAVE_COMMENT)
                
                try:
                    error_dlg = short_wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE_COMMENT))
                    if error_dlg.is_displayed():
                        print(f"-> [LOG] Đã bắt được lỗi Comment ngay khi nhập: '{error_dlg.text}'")
                        self.captured_error_message = error_dlg.text
                        self.click(self.BTN_CANCEL_COMMENT)
                    else:
                        short_wait.until(EC.invisibility_of_element_located(self.BTN_SAVE_COMMENT))
                except TimeoutException:
                    try:
                        short_wait.until(EC.invisibility_of_element_located(self.BTN_SAVE_COMMENT))
                    except: pass
                time.sleep(0.5)
            except TimeoutException:
                pass 
            except Exception as e:
                print(f"Lỗi Comment: {e}")

        # --- 5. SUBMIT ---
        self.click(self.BTN_SAVE)
        time.sleep(0.5)
    def get_status(self):
        return self.get_text(self.STATUS_LABEL)

    