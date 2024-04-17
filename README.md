# Automated Amazon Product Scraper (Autobot)

The **Automated Amazon Product Scraper (Autobot)** is a Python-based tool that automates the process of scraping product data from Amazon. It utilizes Selenium for web scraping and FastAPI to expose a web API for accessing the scraped data.

## Features

- Scrapes product details such as title, price, image URL, and reviews from Amazon.
- Stores scraped data in JSON files for easy access and analysis.
- Provides a FastAPI-based web API to fetch the scraped product data.


### Prerequisites

- Python 3.x installed on your system
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases) for Firefox placed in your system's PATH or in the project directory

## Set up GeckoDriver

Download [GeckoDriver](https://github.com/mozilla/geckodriver/releases) for Firefox and add it to your PATH.

## Create input file

Create a `user_queries.json` file containing product names to scrape.

## Access the web API

After running the script, access the FastAPI web API to fetch scraped product data.

## Dependencies

- Python 3.x
- Selenium
- FastAPI
- Pydantic
- SQLite3
- GeckoDriver

## File Structure

- `main.py`: Entry point of the script that orchestrates the scraping process.
- `api.py`: Defines the FastAPI web API endpoints for fetching scraped data.
- `scraper.py`: Contains the `Scraper` class responsible for scraping product data from Amazon.
- `product.py`: Defines the `Product` class representing a scraped product.
- `dataSaver.py`: Contains the function to save scraped data to JSON files.
- `query_reader.py`: Reads input queries from a JSON file.

## Conclusion

The Amazon Product Scraper system provides a flexible and modular solution for scraping product data from Amazon and exposing it via a web API. By following the provided instructions, users can easily run the script, scrape product data, and access the scraped data through the web API endpoints.

