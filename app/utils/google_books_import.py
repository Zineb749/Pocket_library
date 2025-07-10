
"""
Module pour importer des livres depuis l'API Google Books.

Ce module permet de rechercher des livres via l'API Google Books
et de retourner une liste de livres formatée selon le modèle BookPreview.
"""

import requests
from datetime import datetime
from typing import List
from fastapi import APIRouter, Query, HTTPException
from app.schemas.book import BookPreview  # modèle Pydantic définissant la structure des livres

router = APIRouter()

def fetch_books_from_google(query: str, max_results: int = 5) -> List[dict]:
    """
    Fonction pour récupérer des livres depuis l'API Google Books.

    Args:
        query (str): terme(s) de recherche pour les livres.
        max_results (int): nombre maximum de résultats à récupérer.

    Returns:
        List[dict]: liste de dictionnaires représentant les livres trouvés.

    Lève:
        HTTPException: en cas d'erreur lors de la requête à l'API externe.
    """
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": max_results}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        # Problème réseau ou erreur HTTP, on remonte une erreur 503 au client
        raise HTTPException(status_code=503, detail=f"Error fetching data from Google Books API: {str(e)}")

    data = response.json()

    books = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})

        # Gestion de la date de publication, formats possibles : "YYYY" ou "YYYY-MM-DD"
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

        # Construction du dictionnaire livre avec les champs attendus
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
    """
    Route GET pour importer des livres via une recherche Google Books.

    Args:
        query (str): terme(s) de recherche passé en paramètre URL.

    Retourne:
        Liste des livres correspondant à la recherche, sous forme d'objets BookPreview.
    """
    books_data = fetch_books_from_google(query)
    return books_data
