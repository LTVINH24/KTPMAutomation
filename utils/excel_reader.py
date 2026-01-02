import pandas as pd

def get_data(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str)
        df = df.fillna("") 
        return df.to_dict('records')
    except Exception as e:
        print(f"Lỗi đọc file: {e}")
        return []