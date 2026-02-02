import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, quote


class FragranticaScraper:
    """
    Scraper for Fragrantica.com with fallback to sample data
    Tries to scrape from Fragrantica, falls back to sample data if fails
    """
    
    def __init__(self):
        self.base_url = "https://www.fragrantica.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.driver = None
        
        # Sample perfume database with Fragrantica URLs
        self.sample_data = {
            "Chanel": [
                {
                    "name": "Chanel No. 5 Eau de Parfum",
                    "brand": "Chanel",
                    "designer": "Chanel",
                    "price": 138.00,
                    "size": "50ml",
                    "description": "The ultimate classic fragrance. A timeless, iconic scent that embodies the essence of femininity with its sophisticated floral-aldehyde composition. Created by Ernest Beaux in 1921, it remains the world's most famous perfume.",
                    "notes": "Top: Aldehydes, Neroli, Ylang-ylang | Middle: Rose, Jasmine | Base: Sandalwood, Vanilla, Vetiver",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.6178.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Chanel/Chanel-No-5-6178.html",
                    "rating": 4.5,
                    "gender": "Women",
                    "year": 1921,
                    "top_notes": "Aldehydes, Neroli, Ylang-ylang, Bergamot, Lemon",
                    "middle_notes": "Rose, Jasmine, Lily of the Valley, Iris",
                    "base_notes": "Sandalwood, Vanilla, Vetiver, Patchouli, Musk",
                    "longevity": "Long Lasting (7-12 hours)",
                    "sillage": "Heavy (fills room)"
                },
                {
                    "name": "Coco Mademoiselle Eau de Parfum",
                    "brand": "Chanel",
                    "designer": "Chanel",
                    "price": 125.00,
                    "size": "50ml",
                    "description": "An ambery fragrance, a spirited and voluptuous scent. A daring fragrance with a fresh Oriental signature that captures the irrepressible spirit of a young Coco Chanel.",
                    "notes": "Top: Orange, Bergamot | Middle: Rose, Jasmine, Litchi | Base: Patchouli, Vetiver, Vanilla",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.6115.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Chanel/Coco-Mademoiselle-6115.html",
                    "rating": 4.7,
                    "gender": "Women",
                    "year": 2001,
                    "top_notes": "Orange, Bergamot, Mandarin, Orange Blossom",
                    "middle_notes": "Rose, Jasmine, Litchi, Peach, Ylang-ylang",
                    "base_notes": "Patchouli, Vetiver, Vanilla, White Musk",
                    "longevity": "Very Long Lasting (12+ hours)",
                    "sillage": "Heavy (fills room)"
                },
                {
                    "name": "Bleu de Chanel Eau de Parfum",
                    "brand": "Chanel",
                    "designer": "Chanel",
                    "price": 115.00,
                    "size": "50ml",
                    "description": "A woody-aromatic fragrance that embodies freedom and strength. The scent of a man who charts his own destiny. Fresh, clean, and sophisticated.",
                    "notes": "Top: Grapefruit, Lemon, Mint | Middle: Ginger, Nutmeg, Jasmine | Base: Incense, Cedar, Sandalwood",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.9099.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Chanel/Bleu-de-Chanel-9099.html",
                    "rating": 4.6,
                    "gender": "Men",
                    "year": 2010,
                    "top_notes": "Grapefruit, Lemon, Mint, Pink Pepper",
                    "middle_notes": "Ginger, Nutmeg, Jasmine, Melon, Iso E Super",
                    "base_notes": "Incense, Cedar, Sandalwood, Amber, Patchouli",
                    "longevity": "Long Lasting (7-12 hours)",
                    "sillage": "Moderate (arm's length)"
                }
            ],
            "Dior": [
                {
                    "name": "Dior Sauvage Eau de Parfum",
                    "brand": "Dior",
                    "designer": "Dior",
                    "price": 95.00,
                    "size": "60ml",
                    "description": "A radically fresh composition, dictated by a name that has the ring of a manifesto. Raw and noble, all at once. The powerful freshness of Sauvage reveals new sensual and mysterious facets.",
                    "notes": "Top: Bergamot, Pepper | Middle: Sichuan Pepper, Lavender, Star Anise | Base: Ambroxan, Vanilla, Cedar",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.31881.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Dior/Sauvage-31881.html",
                    "rating": 4.3,
                    "gender": "Men",
                    "year": 2015,
                    "top_notes": "Bergamot, Pepper, Calabrian Lemon",
                    "middle_notes": "Sichuan Pepper, Lavender, Pink Pepper, Vetiver, Patchouli",
                    "base_notes": "Ambroxan, Vanilla, Cedar, Labdanum",
                    "longevity": "Very Long Lasting (12+ hours)",
                    "sillage": "Heavy (fills room)"
                },
                {
                    "name": "Miss Dior Eau de Parfum",
                    "brand": "Dior",
                    "designer": "Dior",
                    "price": 110.00,
                    "size": "50ml",
                    "description": "An exquisite fragrance that embodies the elegance and romance of the Dior woman. A floral bouquet with modern sensuality that celebrates the beauty of centifolia rose.",
                    "notes": "Top: Iris, Peony, Lily of the Valley | Middle: Rose, Lily | Base: Musk, Vanilla, Tonka Bean",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.122155.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Dior/Miss-Dior-122155.html",
                    "rating": 4.4,
                    "gender": "Women",
                    "year": 2021,
                    "top_notes": "Iris, Peony, Lily of the Valley",
                    "middle_notes": "Rose, Lily, Apricot, Peach",
                    "base_notes": "Musk, Vanilla, Tonka Bean, Sandalwood, Vetiver",
                    "longevity": "Moderate (3-6 hours)",
                    "sillage": "Moderate (arm's length)"
                },
                {
                    "name": "J'adore Eau de Parfum",
                    "brand": "Dior",
                    "designer": "Dior",
                    "price": 120.00,
                    "size": "50ml",
                    "description": "A magnificent floral bouquet that celebrates the beauty of flowers. An iconic fragrance that is both sensual and luminous. The ultimate expression of absolute femininity.",
                    "notes": "Top: Pear, Melon, Magnolia | Middle: Jasmine, Lily of the Valley, Tuberose | Base: Musk, Vanilla, Cedar",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.131.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Dior/J-adore-131.html",
                    "rating": 4.5,
                    "gender": "Women",
                    "year": 1999,
                    "top_notes": "Pear, Melon, Magnolia, Peach, Mandarin Orange, Bergamot",
                    "middle_notes": "Jasmine, Lily of the Valley, Tuberose, Freesia, Rose, Orchid, Plum, Violet",
                    "base_notes": "Musk, Vanilla, Cedar, Blackberry",
                    "longevity": "Long Lasting (7-12 hours)",
                    "sillage": "Heavy (fills room)"
                }
            ],
            "Tom Ford": [
                {
                    "name": "Black Orchid Eau de Parfum",
                    "brand": "Tom Ford",
                    "designer": "Tom Ford",
                    "price": 150.00,
                    "size": "50ml",
                    "description": "A luxurious and sensual fragrance with a rich, dark trace of black orchid and spices. Modern and timeless. The first fragrance from Tom Ford, it captures the elusive and mysterious nature of the black orchid.",
                    "notes": "Top: Truffle, Gardenia, Black Currant | Middle: Orchid, Spices, Gardenia | Base: Vanilla, Amber, Sandalwood",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.1825.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Tom-Ford/Black-Orchid-1825.html",
                    "rating": 4.6,
                    "gender": "Women",
                    "year": 2006,
                    "top_notes": "Truffle, Gardenia, Black Currant, Ylang-ylang, Jasmine, Bergamot, Mandarin Orange, Amalfi Lemon",
                    "middle_notes": "Orchid, Spices, Gardenia, Lotus, Fruity Notes, Jasmine",
                    "base_notes": "Vanilla, Amber, Sandalwood, Vetiver, Patchouli, Mexican Chocolate, White Musk",
                    "longevity": "Very Long Lasting (12+ hours)",
                    "sillage": "Enormous (fills entire room)"
                },
                {
                    "name": "Tobacco Vanille Eau de Parfum",
                    "brand": "Tom Ford",
                    "designer": "Tom Ford",
                    "price": 140.00,
                    "size": "50ml",
                    "description": "A rich, spicy, and warm fragrance with notes of tobacco leaf, vanilla, and ginger. Opulent and sophisticated. Part of the Private Blend collection, it's an oriental masterpiece.",
                    "notes": "Top: Tobacco Leaf, Spices | Middle: Vanilla, Cocoa, Tonka Bean | Base: Dried Fruits, Woody Notes",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.1826.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Tom-Ford/Tobacco-Vanille-1826.html",
                    "rating": 4.7,
                    "gender": "Unisex",
                    "year": 2007,
                    "top_notes": "Tobacco Leaf, Ginger, Cumin, Pepper, Coriander, Mandarin Orange, Lemon, Cloves",
                    "middle_notes": "Vanilla, Cocoa, Tonka Bean, Tobacco Blossom",
                    "base_notes": "Dried Fruits, Woody Notes, Syrup, Musk",
                    "longevity": "Very Long Lasting (12+ hours)",
                    "sillage": "Heavy (fills room)"
                },
                {
                    "name": "Oud Wood Eau de Parfum",
                    "brand": "Tom Ford",
                    "designer": "Tom Ford",
                    "price": 155.00,
                    "size": "50ml",
                    "description": "An exotic and distinctive fragrance with rare oud wood, rose wood, and cardamom. Mysterious and compelling. One of the most accessible oud fragrances, perfect for oud beginners.",
                    "notes": "Top: Rose Wood, Cardamom, Chinese Pepper | Middle: Oud Wood, Sandalwood, Vetiver | Base: Vanilla, Amber, Tonka Bean",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.1827.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Tom-Ford/Oud-Wood-1827.html",
                    "rating": 4.5,
                    "gender": "Unisex",
                    "year": 2007,
                    "top_notes": "Rose Wood, Cardamom, Chinese Pepper",
                    "middle_notes": "Oud Wood, Sandalwood, Vetiver",
                    "base_notes": "Vanilla, Amber, Tonka Bean, Musk",
                    "longevity": "Long Lasting (7-12 hours)",
                    "sillage": "Moderate (arm's length)"
                }
            ],
            "Yves Saint Laurent": [
                {
                    "name": "Y Eau de Parfum",
                    "brand": "Yves Saint Laurent",
                    "designer": "Yves Saint Laurent",
                    "price": 95.00,
                    "size": "60ml",
                    "description": "A bold and woody fragrance for the modern man. Fresh and intense with a charismatic signature. The scent of a man who dares to follow his passions.",
                    "notes": "Top: Apple, Ginger | Middle: Sage, Juniper Berries | Base: Amber, Tonka Bean, Cedar",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.49714.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Yves-Saint-Laurent/Y-Eau-de-Parfum-49714.html",
                    "rating": 4.4,
                    "gender": "Men",
                    "year": 2018,
                    "top_notes": "Apple, Ginger, Bergamot, Sage, Juniper Berries",
                    "middle_notes": "Sage, Juniper Berries, Geranium",
                    "base_notes": "Amber, Tonka Bean, Cedar, Oud, Vetiver",
                    "longevity": "Long Lasting (7-12 hours)",
                    "sillage": "Moderate (arm's length)"
                },
                {
                    "name": "Black Opium Eau de Parfum",
                    "brand": "Yves Saint Laurent",
                    "designer": "Yves Saint Laurent",
                    "price": 104.00,
                    "size": "50ml",
                    "description": "A glam rock fragrance for the modern woman. Seductive and addictive with coffee and vanilla notes. The rock'n'roll interpretation of glamour.",
                    "notes": "Top: Pear, Pink Pepper | Middle: Coffee, Jasmine, Orange Blossom | Base: Vanilla, Cedar, Patchouli",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.25324.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Yves-Saint-Laurent/Black-Opium-25324.html",
                    "rating": 4.6,
                    "gender": "Women",
                    "year": 2014,
                    "top_notes": "Pear, Pink Pepper, Orange Blossom, Bergamot",
                    "middle_notes": "Coffee, Jasmine, Bitter Almond, Licorice",
                    "base_notes": "Vanilla, Cedar, Patchouli, Cashmere Wood",
                    "longevity": "Very Long Lasting (12+ hours)",
                    "sillage": "Heavy (fills room)"
                }
            ],
            "Versace": [
                {
                    "name": "Eros Eau de Toilette",
                    "brand": "Versace",
                    "designer": "Versace",
                    "price": 72.00,
                    "size": "50ml",
                    "description": "A fragrance for the man who is heroic and passionate. Fresh and oriental with a masculine signature. Inspired by Greek mythology and the god of love.",
                    "notes": "Top: Mint, Green Apple, Lemon | Middle: Tonka Bean, Ambroxan, Geranium | Base: Madagascar Vanilla, Cedar, Vetiver",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.14923.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Versace/Versace-Eros-14923.html",
                    "rating": 4.3,
                    "gender": "Men",
                    "year": 2012,
                    "top_notes": "Mint, Green Apple, Lemon, Mandarin Orange",
                    "middle_notes": "Tonka Bean, Ambroxan, Geranium",
                    "base_notes": "Madagascar Vanilla, Cedar, Vetiver, Oakmoss",
                    "longevity": "Long Lasting (7-12 hours)",
                    "sillage": "Heavy (fills room)"
                }
            ],
            "Creed": [
                {
                    "name": "Aventus Eau de Parfum",
                    "brand": "Creed",
                    "designer": "Creed",
                    "price": 445.00,
                    "size": "50ml",
                    "description": "A sophisticated and masculine fragrance inspired by the dramatic life of a historic emperor. Bold and powerful. The most popular niche fragrance of all time, known for its pineapple opening.",
                    "notes": "Top: Pineapple, Bergamot, Black Currant | Middle: Birch, Patchouli, Moroccan Jasmine | Base: Musk, Oakmoss, Ambergris, Vanilla",
                    "image_url": "https://fimgs.net/mdimg/perfume/375x500.9828.jpg",
                    "source_url": "https://www.fragrantica.com/perfume/Creed/Aventus-9828.html",
                    "rating": 4.8,
                    "gender": "Men",
                    "year": 2010,
                    "top_notes": "Pineapple, Bergamot, Black Currant, Apple, Lemon",
                    "middle_notes": "Birch, Patchouli, Moroccan Jasmine, Rose",
                    "base_notes": "Musk, Oakmoss, Ambergris, Vanilla, Labdanum",
                    "longevity": "Very Long Lasting (12+ hours)",
                    "sillage": "Enormous (fills entire room)"
                }
            ]
        }
        
        # Generic templates for unknown brands
        self.generic_templates = [
            {
                "name": "Classic Eau de Parfum",
                "price": 85.00,
                "size": "50ml",
                "description": "A timeless classic fragrance with elegant floral notes and warm woody base. Perfect for everyday wear and special occasions.",
                "notes": "Top: Citrus, Bergamot | Middle: Rose, Jasmine | Base: Musk, Vanilla, Cedar",
                "rating": 4.2,
                "gender": "Women",
                "year": 2015,
                "top_notes": "Citrus, Bergamot, Lemon, Mandarin",
                "middle_notes": "Rose, Jasmine, Lily, Ylang-ylang",
                "base_notes": "Musk, Vanilla, Cedar, Sandalwood",
                "longevity": "Moderate (3-6 hours)",
                "sillage": "Moderate (arm's length)"
            },
            {
                "name": "Intense Eau de Toilette",
                "price": 75.00,
                "size": "100ml",
                "description": "An intense and captivating fragrance with spicy and woody accords. Bold and masculine, perfect for the confident man.",
                "notes": "Top: Pepper, Ginger | Middle: Lavender, Geranium | Base: Cedar, Patchouli",
                "rating": 4.0,
                "gender": "Men",
                "year": 2018,
                "top_notes": "Pepper, Ginger, Cardamom, Lemon",
                "middle_notes": "Lavender, Geranium, Sage, Nutmeg",
                "base_notes": "Cedar, Patchouli, Vetiver, Amber",
                "longevity": "Long Lasting (7-12 hours)",
                "sillage": "Moderate (arm's length)"
            },
            {
                "name": "Noir Eau de Parfum",
                "price": 95.00,
                "size": "50ml",
                "description": "A mysterious and seductive fragrance with dark and sensual notes. Unisex appeal with deep, rich accords.",
                "notes": "Top: Bergamot, Black Pepper | Middle: Leather, Iris | Base: Vanilla, Amber, Musk",
                "rating": 4.4,
                "gender": "Unisex",
                "year": 2020,
                "top_notes": "Bergamot, Black Pepper, Grapefruit, Pink Pepper",
                "middle_notes": "Leather, Iris, Styrax, Clary Sage",
                "base_notes": "Vanilla, Amber, Musk, Patchouli, Cedar",
                "longevity": "Very Long Lasting (12+ hours)",
                "sillage": "Heavy (fills room)"
            }
        ]
    
    def setup_selenium(self):
        """Setup Selenium WebDriver with anti-detection measures"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"Error setting up Selenium: {e}")
            return None
    
    def _get_sample_data(self, brand: str, max_items: int = 50) -> List[Dict]:
        """Get sample data for a brand"""
        perfumes = []
        
        # Check if we have sample data for this brand
        if brand in self.sample_data:
            perfumes = self.sample_data[brand][:max_items]
            # Update brand name in each perfume
            for perfume in perfumes:
                perfume["brand"] = brand
                perfume["designer"] = brand
        else:
            # Generate generic perfumes for unknown brands
            for i, template in enumerate(self.generic_templates[:max_items]):
                perfume = template.copy()
                perfume["name"] = f"{brand} {perfume['name']}"
                perfume["brand"] = brand
                perfume["designer"] = brand
                perfume["source_url"] = f"https://www.fragrantica.com/search/?query={brand.replace(' ', '+')}"
                perfumes.append(perfume)
        
        return perfumes
    
    def scrape_by_brand(self, brand: str, max_items: int = 50) -> List[Dict]:
        """
        Try to scrape from Fragrantica, fall back to sample data if fails
        """
        print(f"Attempting to scrape Fragrantica for: {brand}")
        
        # Try to scrape from Fragrantica first
        try:
            search_url = f"{self.base_url}/search/?query={quote(brand)}"
            
            driver = self.setup_selenium()
            if driver:
                driver.get(search_url)
                time.sleep(5)  # Wait for page to load
                
                # Try to find product items
                selectors = [
                    ".perfume-item",
                    ".search-result",
                    ".cell[data-id]",
                    ".grid-x .cell",
                    ".card-fragrance"
                ]
                
                items = []
                for selector in selectors:
                    try:
                        items = driver.find_elements(By.CSS_SELECTOR, selector)
                        if items:
                            print(f"Found {len(items)} items on Fragrantica")
                            break
                    except:
                        continue
                
                driver.quit()
                
                # If we found items, try to extract them
                if items:
                    scraped_perfumes = []
                    for item in items[:max_items]:
                        try:
                            # Try to extract basic info
                            name = ""
                            try:
                                name_elem = item.find_element(By.CSS_SELECTOR, ".fragrance-name, .name, h3 a")
                                name = name_elem.text.strip()
                            except:
                                pass
                            
                            if name:
                                perfume = {
                                    "name": name,
                                    "brand": brand,
                                    "designer": brand,
                                    "price": None,
                                    "size": None,
                                    "description": None,
                                    "notes": None,
                                    "image_url": None,
                                    "source_url": f"https://www.fragrantica.com/search/?query={brand}",
                                    "rating": None,
                                    "gender": None,
                                    "year": None,
                                    "top_notes": None,
                                    "middle_notes": None,
                                    "base_notes": None,
                                    "longevity": None,
                                    "sillage": None
                                }
                                scraped_perfumes.append(perfume)
                        except:
                            continue
                    
                    if scraped_perfumes:
                        print(f"Successfully scraped {len(scraped_perfumes)} perfumes from Fragrantica")
                        return scraped_perfumes
        except Exception as e:
            print(f"Fragrantica scraping failed: {e}")
        
        # Fall back to sample data
        print(f"Using sample data for {brand}")
        return self._get_sample_data(brand, max_items)
    
    def scrape_all_sources(self, brand: str, max_items: int = 50) -> List[Dict]:
        """Main method - tries Fragrantica, falls back to sample data"""
        return self.scrape_by_brand(brand, max_items)


# For backward compatibility with existing code
SimplePerfumeScraper = FragranticaScraper
