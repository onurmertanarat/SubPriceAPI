# Subscription Price Scraping API

A Flask-based REST API that concurrently scrapes the latest subscription prices from major streaming platforms using Selenium.

<p>
  <img src="https://github.com/onurmertanarat/SubPriceAPI/blob/master/assets/subprice-api-screenshot.PNG" alt="API Demo Screenshot">
</p>

---

## Features

* **Concurrent Scraping:** Utilizes a `ThreadPoolExecutor` to scrape multiple websites in parallel, significantly reducing the total execution time compared to a sequential approach.
* **Robust Error Handling:** Implements a retry mechanism that attempts to fetch data multiple times upon failure, making the scraper resilient to temporary network issues or slow page loads.
* **Dynamic & Headless Browser:** Uses Selenium with headless Chrome to scrape dynamic websites that rely on JavaScript to render content.
* **Anti-Scraping Measures:** Rotates `User-Agent` strings for each request using the `fake-useragent` library to mimic real user traffic.
* **Clean Data Extraction:** Parses prices from unstructured text using Regular Expressions (Regex).
* **REST API:** Exposes the scraped data through a clean and simple `/fetch-prices` GET endpoint using the Flask web framework.

---

## Technology Stack

* **Backend:** Flask
* **Web Scraping:** Selenium
* **Concurrency:** `concurrent.futures.ThreadPoolExecutor`
* **Dependencies:** `fake-useragent`, `re`

---

## Installation & Usage

### Prerequisites

* Python 3.8+
* pip
* Google Chrome (or the browser you configure)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/onurmertanarat/SubPriceAPI.git](https://github.com/onurmertanarat/SubPriceAPI.git)
    cd SubPriceAPI
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # Create the environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the API

Run the Flask development server with the following command:

```sh
python app.py
```

The API will be available at http://127.0.0.1:5000.

---

## API Endpoint

```sh
GET /fetch-prices
```

Fetches the latest prices for all configured platforms.

**Method:** GET

**URL:** http://127.0.0.1:5000/fetch-prices

**Success Response (200 OK):**

    [
      {
        "currency": "TRY",
        "name": "Netflix",
        "price": 189.99
      },
      {
        "currency": "TRY",
        "name": "HBO Max",
        "price": 229.9
      },
      {
        "currency": "TRY",
        "name": "MUBI",
        "price": 169.0
      },
      {
        "currency": "TRY",
        "name": "Amazon Prime Video",
        "price": 49.9
      },
      {
        "currency": "TRY",
        "name": "Disney+",
        "price": 349.9
      }
    ]

---

## Contact

Onur Mert Anarat

[linkedin.com/in/onurmertanarat](https://www.linkedin.com/in/onurmertanarat)
