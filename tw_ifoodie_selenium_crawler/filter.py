import csv
from collections import defaultdict

# 建立一個defaultdict來存儲已經處理過的餐廳名稱
processed_restaurants = defaultdict(list)

# 開啟CSV檔案進行讀取
with open('data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # 跳過標題行
    next(csv_reader)
    
    # 遍歷每一行數據
    for row in csv_reader:
        restaurant_title = row[0]
        
        # 如果該餐廳名稱還未被處理過
        if restaurant_title not in processed_restaurants:
            processed_restaurants[restaurant_title].append(row)
        
# 開啟一個新的CSV檔案進行寫入
with open('processed_data.csv', 'w', newline='') as new_file:
    csv_writer = csv.writer(new_file)
    
    # 寫入標題行
    csv_writer.writerow(['restaurant_title', 'restaurant_address', 'restaurant_page', 'restaurant_note', 'restaurant_types'])
    
    # 遍歷已處理過的餐廳名稱
    for restaurant_title, rows in processed_restaurants.items():
        # 只保留第一條記錄
        csv_writer.writerow(rows[0])