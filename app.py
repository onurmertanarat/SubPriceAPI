from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import re
import random
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

platforms = [
    {'name':'Netflix', 'url':'https://www.netflix.com/tr/', 'xpath':'//*[@id="appMountPoint"]/div/div/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div[1]/div/div/p'},
    {'name':'BluTV', 'url':'https://www.blutv.com/', 'xpath':'//*[@id="__next"]/div[3]/div/p[1]'},
    {'name':'Exxen', 'url':'https://www.exxen.com/tr/bilgi/on-bilgilendirme-formu', 'xpath':'/html/body/div[2]/div[4]/p[46]'},
    {'name':'MUBI', 'url':'https://mubi.com/tr/tr/memberships', 'xpath':'//*[@id="__next"]/div[7]/div/table/tbody/tr[1]/td[2]/div[2]/span/div'},
    {'name':'Amazon Prime Video', 'url':'https://www.amazon.com.tr/prime', 'xpath':'//*[@id="prime-hero-header"]/div/div[3]'},
    {'name':'Disney+', 'url':'https://www.disneyplus.com/tr-tr', 'xpath':'/html/body/main/section[1]/div[1]/ul/li[1]/p/span[2]/b'},
]


def fetch_price(platform):
    try:
        ua = UserAgent()
        user_agent = ua.random

        options = Options()
        options.add_argument(f'--user-agent={user_agent}')
        options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1024, 768)

        driver.get(platform['url'])

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, platform['xpath'])))
        price_element = driver.find_element(By.XPATH, platform['xpath'])
        return {'name': platform['name'], 'price_text': price_element.text}
    except (TimeoutException, NoSuchElementException, WebDriverException) as e:
        print(f"Error fetching price from {platform['name']}: {e}")
        return {'name': platform['name'], 'price_text': None}
    finally:
        driver.quit()


def find_price(price_text):
    if not price_text:
        return None
    pattern = r"(?:₺|TL|tl|-\s?TL)\s?(\d{1,3}(?:[.,]\d{1,2})?)|(\d{1,3}(?:[.,]\d{1,2})?)\s?(?:TL|tl|-?\s?TL)"
    matches = re.findall(pattern, price_text)
    prices = []
    for match in matches:
        price = match[0] if match[0] else match[1]
        prices.append(float(price.replace(',', '.')))
    return prices[0] if prices else None

@app.route('/fetch-prices', methods=['GET'])
def fetch_prices():
    currency = request.args.get('currency', 'TRY').upper()
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_price, platforms))
    
    prices = []
    for result in results:
        price = find_price(result['price_text'])
        prices.append({
            'name':result['name'],
            'price':price,
            'currency':currency if price else None
        })
    
    return jsonify(prices)


if __name__ == '__main__':
    app.run(debug=True)