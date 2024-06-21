import csv
import json
import sys
from time import sleep
import time
import traceback
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium import webdriver

from seleniumbase import Driver

class tw_ifoodie_crawler():
    def __init__(self):
        """def get_ChromeOptions(): 
            options = uc.ChromeOptions()
            options.add_argument('--start_maximized')
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument('--headless') 
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-notifications")
            options.add_argument("--incognito")
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--user-data-dir={}".format(os.path.abspath("profile1")))
            return options
        """
        #self.browser_executable_path = ""
        #download_undetected_chromedriver(self.browser_executable_path, undetected=True, arm=False, force_update=True)
        #self.browser_executable_path = os.path.abspath("chromedriver.exe")
        
        #self.driver = uc.Chrome(options=get_ChromeOptions(), executable_path=self.browser_executable_path, version_main=110)
        self.driver = Driver(uc=True, headless=True, agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        
        self.config = self.load_config()    
        self.output_filename = self.config['output_filename']   
        self.get_restaurant_csv()
        self.driver.close()
    def load_config(self, config_file='config.json'):
        with open(config_file, 'r', encoding="utf-8") as file:
            config = json.load(file)
        return config
     
    def get_restaurant_csv(self):
        
        for place in self.config['target_locations']:
            print(f"⭐ {place} ...")
            self.driver.get(f"https://ifoodie.tw/explore/{place}/list")
            time.sleep(1)
            
            try:
                pages = self.driver.find_elements(By.XPATH, "//ul[@class='pagination']/li")
            except:
                pages = 1

            if(len(pages) == 1):
                pages = 1
            elif(len(pages) > 1):
                pages = pages[-2]
                pages = int(pages.get_attribute("textContent"))
            else:
                #此區沒有店
                continue
            
            for page in range(pages):
                def refresh_page():
                    self.driver.get(f"https://ifoodie.tw/explore/{place}/list?page={page}")
                    #self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='jsx-320828271 restaurant-item  track-impression-ga']")))
                    #self.wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='pagination']/li")))
                    #self.wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'title-text')]")))
                    time.sleep(1)
                    self.driver.execute_script("window.stop()")
                    self.driver.switch_to.default_content()
                print("⭐ Page " + str(page) + " ...")
                refresh_page()
                
                restaurants = self.driver.find_elements(By.XPATH, "//div[@class='jsx-320828271 restaurant-item  track-impression-ga']")
                scroll_box = self.driver.find_element(By.CSS_SELECTOR, '#search-scroll-box')
                print(len(restaurants))
                count = 0
                
                for restaurant in restaurants:
                    # 獲取JavaScriptExecutor
                    js = self.driver.execute_script
                    # 這將scroll box滾動到底部
                    js("arguments[0].scrollTop = 1000", scroll_box)
                    
                    count += 1
                    print(f"⭐ Restaurant {count} / {len(restaurants)} ...")
                    try:
                        restaurant_note = restaurant.find_element(By.XPATH, ".//div[contains(@class, 'primary-checkin')]/a").get_attribute("href")
                    except:
                        restaurant_note = ""


                    try:
                        restaurant_info = restaurant.find_elements(By.XPATH, ".//a")

                        restaurant_title = restaurant_info[2].get_attribute("textContent")
                        restaurant_types = []
                        restaurant_types_list = restaurant.find_elements(By.XPATH, ".//a[contains(@class, 'category')]")
                        for r in restaurant_types_list:
                            if r.get_attribute("textContent") != "附近餐廳":
                                restaurant_types.append(r.get_attribute("textContent"))
                        restaurant_address = restaurant.find_element(By.XPATH, ".//div[contains(@class, 'address-row')]").get_attribute("textContent")
                        restaurant_page = restaurant.find_element(By.XPATH, ".//a[contains(@class, 'title-text')]").get_attribute("href") 
                        
                        print(restaurant_title, restaurant_address, restaurant_page, restaurant_note, restaurant_types)
                    except Exception as e:
                        
                        print(f"Error: {type(e).__name__} - {str(e)}")
                        traceback_str = traceback.format_exc()
                        print(traceback_str)
                        
                        
                        #print(restaurant.get_attribute("outerHTML"))
                        
                        self.driver.get_screenshot_as_file("screenshot.png")
                        
                        self.driver.switch_to.default_content()
                        iframes = self.driver.find_elements(By.TAG_NAME, ("iframe"))
                        for iframe in iframes:
                            # 切換到當前iframe
                            self.driver.switch_to.frame(iframe)
                            
                            # 嘗試在當前iframe中找到目標元素
                            try:
                                element = self.driver.find_element(By.XPATH, "//div[@class='jsx-320828271 restaurant-item  track-impression-ga']")
                                print("元素找到在iframe:", iframe)
                                # 執行其他操作...
                                break
                            except:
                                # 如果在當前iframe中找不到元素,切換回上層
                                self.driver.switch_to.default_content()
                        
                        sys.exit()
                        #print(restaurant.get_attribute("outerHTML"))

                            
                
                    with open(self.output_filename, mode='a', encoding='utf-8', newline='') as csv_file:
                        fieldnames = ["restaurant_title", "restaurant_address", "restaurant_page", "restaurant_note", "restaurant_types"]
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        # Check if the file is empty, if so, write the header
                        csv_file.seek(0, 2)  # Move to the end of file
                        if csv_file.tell() == 0:  # Check file position
                            writer.writeheader()
                        
                        data = {
                            "restaurant_title": restaurant_title,
                            "restaurant_address": restaurant_address,
                            "restaurant_page": restaurant_page,
                            "restaurant_note": restaurant_note,
                            "restaurant_types": restaurant_types
                        }
                        writer.writerow(data)
    
crawler = tw_ifoodie_crawler()
