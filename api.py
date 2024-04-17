from typing import List
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from scraper import Scraper
from data_saver import save_to_json
from product import Product
import sqlite3
import uuid
from datetime import datetime

app = FastAPI()

# SQLite Database Initialization
conn = sqlite3.connect('scraped_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS scraped_products
             (request_id TEXT PRIMARY KEY,
              product_title TEXT,
              product_price TEXT,
              product_image_url TEXT,
              product_reviews TEXT,
              timestamp TEXT)''')
conn.commit()

class Query(BaseModel):
    query: str

class ProductResponse(BaseModel):
    title: str
    price: str
    image_url: str
    reviews: str
    timestamp: str

class RequestID(BaseModel):
    request_id: str

@app.post("/fetch_query/", response_model=RequestID)
async def fetch_query(query: Query, background_tasks: BackgroundTasks):
    request_id = str(uuid.uuid4())
    background_tasks.add_task(scrape_data, query.query, request_id)
    return RequestID(request_id=request_id)

@app.get("/fetch_data/{request_id}", response_model=List[ProductResponse])
async def fetch_data(request_id: str):
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM scraped_products WHERE request_id=?", (request_id,))
    rows = c.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Data not found")
    products = []
    for row in rows:
        product = ProductResponse(title=row[1], price=row[2], image_url=row[3], reviews=row[4], timestamp=row[5])
        products.append(product)
    return products

def scrape_data(query: str, request_id: str):
    scraper = Scraper()
    product_data = scraper.fetch_product_data(query)
    for title, data in product_data.items():
        save_to_database(request_id, title, data)
    scraper.QuitDriver()

def save_to_database(request_id: str, title: str, data: dict):
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO scraped_products (request_id, product_title, product_price, product_image_url, product_reviews, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (request_id, title, data["price"], data["image_url"], data["reviews"], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
