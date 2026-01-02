import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.login_page import LoginPage
from pages.time_page import TimePage
from utils.excel_reader import get_data
from dotenv import load_dotenv
import os
load_dotenv()
@pytest.mark.usefixtures("driver")
class TestUC02State:
    current_role = None 
    def parse_input_string(self, input_str):
        data = {"Project": "", "Activity": "", "Time": "", "Comment": ""}
        if not input_str: return data
        parts = input_str.split(',')
        for part in parts:
            if ":" in part:
                key, value = part.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key == "Project": data["Project"] = value
                if key == "Activity": data["Activity"] = value
                if key == "Time": data["Time"] = value
                if key == "Comment": data["Comment"] = value
        return data

    @pytest.mark.parametrize("data", get_data("data/Input_Data.xlsx", "UC02_Timesheet_State"))
    def test_timesheet_state_transition(self, driver, data):
        print(f"\nTesting {data['Test Case ID']} ({data['User Role']}): {data['Action']}")
        emp_user = data["Username"]
        emp_pass = os.getenv("EMPLOYEE_PASS")
        emp_name_for_admin =data["EmpNameForAdminSearch"]
        logout = data["Logout"]
        lp = LoginPage(driver)
        tp = TimePage(driver)
        
        required_role = data['User Role'] 

        
        if self.current_role != required_role or logout == "Yes":
            
            if self.current_role is not None:
                lp.logout()
            lp.login(emp_user, emp_pass)
            TestUC02State.current_role = required_role

        if required_role == "Admin":
            driver.get("http://localhost:8080/web/index.php/time/viewEmployeeTimesheet")
            time.sleep(2)
        
            try:
                emp_input = driver.find_element(By.XPATH, "//input[@placeholder='Type for hints...']")
                current_val = emp_input.get_attribute("value")
                if emp_name_for_admin not in current_val: 
                    emp_input.send_keys(emp_name_for_admin) 
                    time.sleep(2)
                    emp_input.send_keys(Keys.ARROW_DOWN)
                    emp_input.send_keys(Keys.ENTER)
                    driver.find_element(By.XPATH, "//button[@type='submit']").click()
                    time.sleep(1)
            except:
                pass
        else:
            tp.navigate_my_timesheet()

        action = data['Action']
        parsed_input = self.parse_input_string(data['Input Data'])

        try:
            if "Create" in action or "Edit" in action:
                tp.create_timesheet_entry(
                    project=parsed_input['Project'], 
                    activity=parsed_input['Activity'], 
                    time_val=parsed_input['Time'],
                    comment=parsed_input['Comment']
                )
            elif action == "Submit":
                tp.click(tp.BTN_SUBMIT)
            elif action == "Approve":
                tp.click(tp.BTN_APPROVE)
            elif action == "Reject":
                tp.click(tp.BTN_REJECT)
            time.sleep(2) 
            actual_status = tp.get_status()
            print(f"Expected: {data['Expected Status']} | Actual: {actual_status}")
            assert data['Expected Status'] in actual_status
        
        except Exception as e:
            print(f"Test Fail! Reset trạng thái login. Lỗi: {e}")
            TestUC02State.current_role = None
            try:
                lp.logout() 
            except:
                pass
            raise e 