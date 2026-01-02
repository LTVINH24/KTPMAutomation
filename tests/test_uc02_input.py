import pytest
import time
from pages.login_page import LoginPage
from pages.time_page import TimePage
from utils.excel_reader import get_data
from dotenv import load_dotenv
import os
load_dotenv()
@pytest.mark.usefixtures("driver")
class TestUC02Input:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, driver, request):
        request.cls.login_page = LoginPage(driver)
        request.cls.time_page = TimePage(driver)
        emp_user = os.getenv("EMPLOYEE_USER")
        emp_pass = os.getenv("EMPLOYEE_PASS")
        request.cls.login_page.login(emp_user, emp_pass)

    @pytest.mark.parametrize("data", get_data("data/Input_Data.xlsx", "UC02_Timesheet"))
    def test_timesheet_input_validation(self, driver, data):        
        print(f"\nRunning TC: {data['Test Case ID']}")
        
        self.time_page.navigate_my_timesheet()
        
        self.time_page.create_timesheet_entry(
            project=data['Project'], 
            activity=data['Activity'], 
            time_val=data['Time'],
            comment=data.get('Comment')
        )

        expected = str(data['Expected Result']).lower()
        actual_message = self.time_page.get_toast_message()
        
        # --- CASE THÀNH CÔNG ---
        if "thành công" in expected:
            assert "Successfully Saved" in actual_message
        
        # --- CASE LỖI (Quan trọng) ---
        else:
            error_keywords = [
                "should be less than", "decimal format", 
                "select a project", "select an activity",
                "required", "invalid", "no record", "format", "exceeds",
                "should not"
            ]
           
            error_captured = self.time_page.captured_error_message.lower()            
            found_captured_error = False
    
            for err in error_keywords:
                if err in error_captured:
                    found_captured_error = True
                    print(f"-> [PASS] Đã bắt được lỗi (Captured): '{err}'")
                    break
            if found_captured_error:
                assert True
                return
            

            page_source_lower = driver.page_source.lower()
            found_ui_error = False
            for err in error_keywords:
                if err in page_source_lower:
                    found_ui_error = True
                    print(f"-> [PASS] Tìm thấy lỗi trên màn hình (UI): '{err}'")
                    break
            
            if found_ui_error:
                assert True
                return
            
        
            elif "Successfully Saved" in actual_message:
                pytest.fail(f"FAIL: Mong đợi lỗi '{expected}' nhưng hệ thống lại báo 'Successfully Saved' và không tìm thấy thông báo lỗi nào!")
            
            # Cuối cùng: Không Success, cũng không thấy lỗi -> FAIL
            pytest.fail(f"FAIL: Mong đợi lỗi '{expected}' nhưng không thấy hiển thị!")