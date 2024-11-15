# Subscription Price Fetcher API

This project is a Flask-based web application that fetches subscription prices from popular streaming platforms using Selenium.

## Screenshots
### API Example
![API Response Example](https://github.com/onurmertanarat/SubPriceAPI/blob/master/screenshots/api_example.PNG)

### Browser View
![Browser View](https://github.com/onurmertanarat/SubPriceAPI/blob/master/screenshots/browser_view.PNG)


## Features
- Fetches subscription prices from platforms like Netflix, BluTV, Exxen, MUBI, and more.
- Uses multithreading for efficient scraping.
- Returns results in JSON format.

## Installation
1. Clone the repository:
   ```bash
    git clone https://github.com/username/subscription-price-fetcher.git
    cd subscription-price-fetcher
    ```
2. Install dependencies:
   ```bash
    pip install -r requirements.txt
    ```
3. Ensure ChromeDriver is installed and accessible in your system's PATH.

## How to Install ChromeDriver
ChromeDriver must match the version of Google Chrome installed on your system. Follow the steps below to install it:
1. Download ChromeDriver from the official site: https://chromedriver.chromium.org/downloads
2. Extract the downloaded file and add the directory containing chromedriver.exe to your system's PATH variable.

## Usage
1. Run the Flask application:
   ```bash
   python app.py
    ```
2. Access the API at:
   ```bash
   http://127.0.0.1:5000/fetch-prices
    ```
   
## Notes
- Ensure you have the correct version of ChromeDriver matching your Chrome browser version.
- This project is for educational purposes only and should comply with the terms of service of the platforms being scraped.

## License
This project is licensed under a **Proprietary License**. Unauthorized use, distribution, or modification of the code is strictly prohibited.
