import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from typing import List, Dict
from src.models.perfume import PerfumeCreate

class PerfumeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def setup_selenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            print(f"Error setting up Selenium: {e}")
            return None
    
    def scrape_sephora(self, brand: str, max_items: int = 50) -> List[Dict]:
        """Scrape perfume data from Sephora"""
        perfumes = []
        
        try:
            search_url = f"https://www.sephora.com/search?keyword={brand.replace(' ', '%20')}%20perfume"
            
            driver = self.setup_selenium()
            if not driver:
                return perfumes
                
            driver.get(search_url)
            time.sleep(3)
            
            # Scroll to load more items
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Find perfume items
            items = driver.find_elements(By.CSS_SELECTOR, "[data-comp='ProductCard']")
            
            for i, item in enumerate(items[:max_items]):
                try:
                    perfume_data = self._extract_sephora_item(item, brand)
                    if perfume_data:
                        perfumes.append(perfume_data)
                except Exception as e:
                    print(f"Error extracting item {i}: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            print(f"Error scraping Sephora: {e}")
        
        return perfumes
    
    def _extract_sephora_item(self, item, brand: str) -> Dict:
        """Extract data from a single Sephora item"""
        try:
            # Name and brand
            name_elem = item.find_element(By.CSS_SELECTOR, "[data-comp='ProductTitle']")
            name = name_elem.text.strip() if name_elem else ""
            
            # Price
            price_elem = item.find_element(By.CSS_SELECTOR, "[data-comp='Price']")
            price_text = price_elem.text.strip() if price_elem else ""
            price = self._extract_price(price_text)
            
            # Image
            img_elem = item.find_element(By.CSS_SELECTOR, "img")
            image_url = img_elem.get_attribute("src") if img_elem else ""
            
            # Product link
            link_elem = item.find_element(By.CSS_SELECTOR, "a")
            product_url = link_elem.get_attribute("href") if link_elem else ""
            if product_url and not product_url.startswith("http"):
                product_url = f"https://www.sephora.com{product_url}"
            
            return {
                "name": name,
                "brand": brand,
                "designer": brand,
                "price": price,
                "size": None,
                "description": None,
                "notes": None,
                "image_url": image_url,
                "source_url": product_url
            }
            
        except Exception as e:
            print(f"Error extracting item data: {e}")
            return None
    
    def scrape_fragrancex(self, brand: str, max_items: int = 50) -> List[Dict]:
        """Scrape perfume data from FragranceX"""
        perfumes = []
        
        try:
            search_url = f"https://www.fragrancex.com/search/{brand.replace(' ', '-')}-perfume.html"
            
            driver = self.setup_selenium()
            if not driver:
                return perfumes
                
            driver.get(search_url)
            time.sleep(3)
            
            # Find perfume items
            items = driver.find_elements(By.CSS_SELECTOR, ".product-item")
            
            for i, item in enumerate(items[:max_items]):
                try:
                    perfume_data = self._extract_fragrancex_item(item, brand)
                    if perfume_data:
                        perfumes.append(perfume_data)
                except Exception as e:
                    print(f"Error extracting item {i}: {e}")
                    continue
            
            driver.quit()
            
        except Exception as e:
            print(f"Error scraping FragranceX: {e}")
        
        return perfumes
    
    def _extract_fragrancex_item(self, item, brand: str) -> Dict:
        """Extract data from a single FragranceX item"""
        try:
            # Name
            name_elem = item.find_element(By.CSS_SELECTOR, ".product-name")
            name = name_elem.text.strip() if name_elem else ""
            
            # Price
            price_elem = item.find_element(By.CSS_SELECTOR, ".price")
            price_text = price_elem.text.strip() if price_elem else ""
            price = self._extract_price(price_text)
            
            # Image
            img_elem = item.find_element(By.CSS_SELECTOR, ".product-image img")
            image_url = img_elem.get_attribute("src") if img_elem else ""
            
            # Product link
            link_elem = item.find_element(By.CSS_SELECTOR, ".product-link")
            product_url = link_elem.get_attribute("href") if link_elem else ""
            
            return {
                "name": name,
                "brand": brand,
                "designer": brand,
                "price": price,
                "size": None,
                "description": None,
                "notes": None,
                "image_url": image_url,
                "source_url": product_url
            }
            
        except Exception as e:
            print(f"Error extracting item data: {e}")
            return None
    
    def _extract_price(self, price_text: str) -> float:
        """Extract numeric price from price text"""
        try:
            import re
            price_match = re.search(r'\$?(\d+\.?\d*)', price_text.replace(',', ''))
            if price_match:
                return float(price_match.group(1))
        except:
            pass
        return None
    
    def scrape_all_sources(self, brand: str, max_items: int = 50) -> List[Dict]:
        """Scrape from multiple sources"""
        all_perfumes = []
        
        # Scrape from Sephora
        sephora_perfumes = self.scrape_sephora(brand, max_items // 2)
        all_perfumes.extend(sephora_perfumes)
        
        # Scrape from FragranceX
        fragrancex_perfumes = self.scrape_fragrancex(brand, max_items // 2)
        all_perfumes.extend(fragrancex_perfumes)
        
        return all_perfumes