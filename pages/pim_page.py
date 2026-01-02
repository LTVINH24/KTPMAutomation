from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys  
import time

class PIMPage(BasePage):
    MENU_PIM = (By.LINK_TEXT, "PIM")
    BTN_ADD = (By.XPATH, "//button[text()=' Add ']")
    
    # Form Fields
    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    MIDDLE_NAME = (By.NAME, "middleName")
    EMP_ID = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")
    
    # Login Details
    SWITCH_LOGIN = (By.XPATH, "//p[text()='Create Login Details']/../div//span")
    USERNAME = (By.XPATH, "//label[text()='Username']/../following-sibling::div//input")
    PASSWORD = (By.XPATH, "//label[text()='Password']/../following-sibling::div//input")
    CONFIRM_PASS = (By.XPATH, "//label[text()='Confirm Password']/../following-sibling::div//input")
    
    BTN_SAVE = (By.XPATH, "//button[@type='submit']")

    def navigate_add_employee(self):
        self.click(self.MENU_PIM)
        self.click(self.BTN_ADD)

    def fill_employee_form(self, data):
        self.send_keys(self.FIRST_NAME, data['First Name'])
        self.send_keys(self.MIDDLE_NAME, data['Middle Name'])
        self.send_keys(self.LAST_NAME, data['Last Name'])
        self.send_keys(self.EMP_ID, data['Employee Id'])
        if data['Create Login'] == 'Yes':
            self.click(self.SWITCH_LOGIN)
            self.send_keys(self.USERNAME, data['Username'])
            self.send_keys(self.PASSWORD, data['Password'])
            self.send_keys(self.CONFIRM_PASS, data['Confirm Password'])
        
        self.click(self.BTN_SAVE)