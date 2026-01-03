# KTPM - Công cụ automation testing cho OrangeHRM

## 🛠️ Cài đặt

```bash
# 1. Clone repo hoặc mở thư mục source code
git clone https://github.com/LTVINH24/KTPMAutomation.git

# 2 Tạo venv
python -m venv venv
.\venv\Scripts\activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Cấu hình database
cp .env.example .env
# Chỉnh sửa .env theo cấu hình của bạn
```
---

## 🚀 Chạy Automation Testing


```bash
python -m pytest --browser=chrome --html=report.html --self-contained-html
```
### --browser: chrome/firefox/edge
### --html: tên file báo cáo kết quả test

## 🔐 Thông tin mặc định

| Thông tin | Giá trị |
|-----------|---------|
| Mật khẩu user | `OrangeHRM@111` |
 |
| OrangeHRM | http://localhost:8080 |
