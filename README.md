# 台灣愛食記餐廳爬蟲

這個專案是一個網頁爬蟲，用於從台灣愛食記網站（ifoodie.tw）收集餐廳資訊。

## 功能

- 從指定地點爬取餐廳列表
- 提取餐廳詳細資訊
- 處理和去重收集到的數據

## 檔案說明

- `main.py`: 主要爬蟲腳本
- `config.json`: 配置文件，包含目標地點和輸出文件名
- `extract_page.py`: 提取餐廳食紀的腳本
- `filter.py`: 處理和去重數據的腳本

## 使用方法

1. 安裝依賴：
`pip install seleniumbase`

2. 在 `config.json` 中設置目標地點

3. 運行主要爬蟲：
`python main.py`

4. 處理數據：
`python filter.py`

5. 提取詳細資訊（可選）：
`python extract_page.py`

## 輸出

- `data.csv`: 原始爬取數據
- `processed_data.csv`: 去重後的數據
- `note.csv`: 餐廳詳細食紀抓取（如果使用 extract_page.py）

## 注意事項

請遵守網站使用條款和爬蟲政策，設置適當的爬取延遲以避免對目標網站造成過大負擔。
