from query_reader import read_queries
from scraper import Scraper
from data_saver import save_to_json

def main():
    queries = read_queries()

    if queries:
        scraper = Scraper()
        for query in queries:
            Product_details = scraper.fetch_product_data(query)
            save_to_json(Product_details, query + '.json')
        scraper.QuitDriver()
    else:
        print("No queries found.")

if __name__ == "__main__":
    main()
 