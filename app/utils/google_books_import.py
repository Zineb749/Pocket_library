import requests
from datetime import datetime
from typing import List
from fastapi import APIRouter, Query, HTTPException
from app.schemas.book import BookPreview  # modèle à créer (voir ci-dessous)

router = APIRouter()

def fetch_books_from_google(query: str, max_results: int = 5) -> List[dict]:
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": max_results}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error fetching data from Google Books API: {str(e)}")

    data = response.json()

    books = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        pub_date = volume_info.get("publishedDate", None)
        try:
            if pub_date and len(pub_date) == 4:
                pub_date = datetime.strptime(pub_date, "%Y").date()
            elif pub_date and len(pub_date) >= 7:
                pub_date = datetime.strptime(pub_date[:10], "%Y-%m-%d").date()
            else:
                pub_date = None
        except Exception:
            pub_date = None

        book = {
            "title": volume_info.get("title", "No title"),
            "author": ", ".join(volume_info.get("authors", ["Unknown"])),
            "description": volume_info.get("description"),
            "purchase_date": pub_date,
            "cover_url": volume_info.get("imageLinks", {}).get("thumbnail")
        }
        books.append(book)
    return books

@router.get("/", response_model=List[BookPreview])
def import_google_books(query: str = Query(..., min_length=1)):
    books_data = fetch_books_from_google(query)
    return books_data
