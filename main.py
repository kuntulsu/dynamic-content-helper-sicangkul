import requests
from bs4 import BeautifulSoup

from fastapi import FastAPI

app = FastAPI()


def _fetch_articles(page=1):
    url = f"https://pecangaankulon.jepara.go.id?page={page}"
    response = requests.Session()
    response.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })
    response = response.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article")
        return articles

@app.get("/api/articles")
async def get_articles(page: int = 1):
    articles = _fetch_articles(page)
    if articles:
        result = []
        for article in articles:
            thumbnail = article.find("img").get("src")
            title = article.find(class_="text-heading").a.text.strip()
            subtitle = article.find("p").text.strip()
            result.append({
                "thumbnail": thumbnail,
                "title": title,
                "subtitle": subtitle
            })
        return {"articles": result}
    else:
        return {"message": "No articles found."}


def _fetch_lapak(page=1):
    url = f"https://pecangaankulon.jepara.go.id/internal_api/lapak/produk?page[number]=2"
    response = requests.Session()
    response.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })
    response = response.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])

@app.get("/api/lapak")
async def get_lapak(page: int = 1):
    lapak_items = _fetch_lapak(page)
    if lapak_items:
        result = []
        for item in lapak_items:
            thumbnail = item["attributes"].get("foto")[0]
            title = item["attributes"].get("nama")
            subtitle = item["attributes"].get("deskripsi")
            seller = item["attributes"]["pelapak"]["penduduk"].get("nama")
    
            result.append({
                "thumbnail": thumbnail,
                "title": title,
                "subtitle": subtitle,
                "seller": seller
            })
        return {"lapak_items": result}
    else:
        return {"message": "No lapak items found."}
