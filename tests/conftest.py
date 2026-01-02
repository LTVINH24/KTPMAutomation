import pytest
from selenium import webdriver

# Thêm tùy chọn dòng lệnh để chọn trình duyệt
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome, firefox, edge")

@pytest.fixture(scope="class")
def driver(request):
    browser_name = request.config.getoption("--browser")
    
    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError("Browser not supported!")

    driver.maximize_window()
    # driver.implicitly_wait(10)
    
    yield driver
    driver.quit()