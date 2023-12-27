

import os
import pandas as pd

directory_path = r'D:\Scraping\Out'

file_list = os.listdir(directory_path)

content_list = []

for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        content_list.append(content)

df = pd.DataFrame({'Content': content_list})

excel_file_path = r'D:\Scraping\output.xlsx'
df.to_excel(excel_file_path, index=False)
