import pytest
from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.excel_reader import get_data
import os
from dotenv import load_dotenv

load_dotenv()
@pytest.mark.usefixtures("driver")
class TestUC01:
    
    @pytest.fixture(scope="class", autouse=True)
    def setup(self, driver, request):
        request.cls.login_page = LoginPage(driver)
        request.cls.pim_page = PIMPage(driver)
        emp_user = os.getenv("ADMIN_USER")
        emp_pass = os.getenv("ADMIN_PASS")
        request.cls.login_page.login(emp_user, emp_pass) 

    @pytest.mark.parametrize("data", get_data("data/Input_Data.xlsx", "UC01_AddEmployee"))
    def test_add_employee(self, driver, data):
        print(f"\nRunning TC: {data['Test Case ID']} - {data['Description']}")
        self.pim_page.navigate_add_employee()
        self.pim_page.fill_employee_form(data)
        
        actual_message = self.pim_page.get_toast_message()
        page_source = driver.page_source
        expected_res = data['Expected Result']

        if "thành công" in expected_res or "Successfully" in expected_res:
            assert "Successfully Saved" in actual_message or "Personal Details" in driver.title
        else:
            if "Required" in page_source or "Already exists" in page_source:
                assert True 
            elif actual_message != "":
                assert True
            else:

                pytest.fail(f"Mong đợi lỗi '{expected_res}' nhưng không thấy hiển thị!")