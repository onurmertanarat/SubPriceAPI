from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import re
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

platforms = [
    {'name':'Netflix', 'url':'https://www.netflix.com/tr/', 'by': By.XPATH, 'selector': "//p[contains(text(), 'TL ile başlayan fiyatlarla')]"},
    {'name':'HBO Max', 'url':'https://www.hbomax.com/tr/tr', 'by': By.XPATH, 'selector': "//h4[contains(., 'TL') and em[contains(text(), '/ay')]]"},
    {'name':'MUBI', 'url':'https://mubi.com/tr/tr/memberships', 'by': By.XPATH, 'selector': "//div[starts-with(text(), '₺')]"},
    {'name':'Amazon Prime Video', 'url':'https://www.amazon.com.tr/prime', 'by': By.XPATH, 'selector': "//span[contains(text(), 'sonrasında Prime')]"},
    {'name':'Disney+', 'url':'https://www.disneyplus.com/tr-tr', 'by': By.XPATH, 'selector': "//p[contains(text(), 'TL / ay')]"},
]

def fetch_price(platform, retries=3, delay=5):
    for attempt in range(retries):
        driver = None
        try:
            ua = UserAgent()
            user_agent = ua.random

            options = Options()
            options.add_argument(f'--user-agent={user_agent}')
            options.add_argument('--headless')
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--log-level=3")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--blink-settings=imagesEnabled=false')

            driver = webdriver.Chrome(options=options)
            driver.get(platform['url'])

            wait_condition = EC.visibility_of_element_located((platform['by'], platform['selector']))
            WebDriverWait(driver, 15).until(wait_condition) 
            price_element = driver.find_element(platform['by'], platform['selector'])
            
            return {'name': platform['name'], 'price_text': price_element.text}

        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            print(f"Attempt {attempt + 1}/{retries} for {platform['name']} failed. Retrying in {delay}s...")
            time.sleep(delay)
        
        finally:
            if driver:
                driver.quit()

    print(f"All {retries} attempts for {platform['name']} failed.")
    return {'name': platform['name'], 'price_text': None}


def find_price(price_text):
    if not price_text:
        return None
    pattern = r'(\d{1,3}[.,]\d{2})'
    matches = re.findall(pattern, price_text)
    
    if not matches:
        pattern = r'(\d+)'
        matches = re.findall(pattern, price_text)

    if matches:
        price = matches[0].replace(',', '.')
        return float(price)
    return None

@app.route('/fetch-prices', methods=['GET'])
def fetch_prices():
    currency = request.args.get('currency', 'TRY').upper()
    
    with ThreadPoolExecutor(max_workers=len(platforms)) as executor:
        results = list(executor.map(fetch_price, platforms))
    
    prices = []
    for result in results:
        price = find_price(result['price_text'])
        prices.append({
            'name': result['name'],
            'price': price,
            'currency': currency if price else None
        })
    
    return jsonify(prices)


if __name__ == '__main__':
    app.run(debug=True)