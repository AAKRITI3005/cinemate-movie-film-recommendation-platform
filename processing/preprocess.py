import requests
import streamlit as st
import time
import os
import json

#  API KEYS 
TMDB_API_KEY = "b50b67d9b53fe14bccfd5d0e2e6fad58"  # TMDb
OMDB_API_KEY = "63d2795c"                           # OMDb

TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w500"


WISHLIST_PATH = os.path.join(os.path.dirname(__file__), "..", "wishlist.json")


def safe_request(url, retries=3, delay=3):
    """
    Makes an API request safely with retries and error handling.
    Prevents Streamlit app from breaking if connection is lost.
    """
    for i in range(retries):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"[TMDB] Timeout, retrying {i+1}/{retries} ...")
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"[TMDB] Request failed (attempt {i+1}/{retries}): {e}")
            time.sleep(delay)
    return None


def _img(path):
    return f"{TMDB_IMG_BASE}{path}" if path else None

def load_wishlist():
    """Load wishlist from local JSON file (if exists)."""
    if not os.path.exists(WISHLIST_PATH):
        return []
    try:
        with open(WISHLIST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except Exception as e:
        print("[WISHLIST] Error loading wishlist:", e)
        return []


def save_wishlist(wishlist):
    """Save wishlist list of dicts to local JSON file."""
    try:
        with open(WISHLIST_PATH, "w", encoding="utf-8") as f:
            json.dump(wishlist, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[WISHLIST] Error saving wishlist:", e)



@st.cache_data(ttl=3600)
def tmdb_popular_titles(pages=3):
    """Fetch many popular titles (for dropdowns & grids)."""
    results = []
    for p in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={p}"
        data = safe_request(url)
        if not data:
            continue
        for m in data.get("results", []):
            title = m.get("title") or m.get("name")
            year = (m.get("release_date") or "")[:4]
            results.append({
                "id": m.get("id"),
                "title": title,
                "label": f"{title} ({year})" if year else title
            })
    # remove duplicates
    seen = set()
    uniq = []
    for r in results:
        k = (r["id"], r["title"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    return uniq


@st.cache_data(ttl=3600)
def tmdb_search(query, max_pages=2):
    """Search TMDb dynamically when the user types."""
    out = []
    q = query.strip()
    if not q:
        return out
    for p in range(1, max_pages + 1):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={q}&language=en-US&page={p}"
        data = safe_request(url)
        if not data:
            continue
        for m in data.get("results", []):
            title = m.get("title") or m.get("name")
            year = (m.get("release_date") or "")[:4]
            out.append({
                "id": m.get("id"),
                "title": title,
                "label": f"{title} ({year})" if year else title
            })
    # remove duplicates
    seen = set()
    uniq = []
    for r in out:
        k = (r["id"], r["title"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    return uniq


@st.cache_data(ttl=3600)
def tmdb_similar_by_id(movie_id):
    """Fetch similar movies from TMDb."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={TMDB_API_KEY}&language=en-US&page=1"
    res = safe_request(url)
    if not res:
        return []
    sims = []
    for m in res.get("results", [])[:10]:
        sims.append({
            "id": m.get("id"),
            "title": m.get("title"),
            "overview": m.get("overview"),
            "rating": m.get("vote_average"),
            "poster": _img(m.get("poster_path"))
        })
    return sims



@st.cache_data(ttl=3600)
def tmdb_id_for_title(title):
    """Find the first matching movie ID for a given title."""
    data = tmdb_search(title, max_pages=1)
    return data[0]["id"] if data else None

@st.cache_data(ttl=3600)
def omdb_details(title):
    """Fetch details from OMDb API."""
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    r = safe_request(url)
    if r and r.get("Response") == "True":
        return {
            "title": r.get("Title"),
            "year": r.get("Year"),
            "genre": r.get("Genre"),
            "plot": r.get("Plot"),
            "imdb": r.get("imdbRating"),
            "poster": r.get("Poster") if r.get("Poster") and r.get("Poster") != "N/A" else None,
            "actors": r.get("Actors"),
            "director": r.get("Director")
        }
    return None



@st.cache_data(ttl=3600)
def tmdb_details_by_id(movie_id):
    """Fetch detailed info from TMDb using movie ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    r = safe_request(url)
    if r and r.get("id"):
        genres = ", ".join([g["name"] for g in r.get("genres", [])])
        return {
            "id": r.get("id"),
            "title": r.get("title"),
            "year": (r.get("release_date") or "")[:4],
            "genre": genres,
            "plot": r.get("overview"),
            "imdb": r.get("vote_average"),
            "poster": _img(r.get("poster_path")),
            "actors": "—",
            "director": "—"
        }
    return None


@st.cache_data(ttl=3600)
def describe_movie(title):
    """Try OMDb first; if it fails, fallback to TMDb."""
    d = omdb_details(title)
    if d:
        return d
    movie_id = tmdb_id_for_title(title)
    if movie_id:
        return tmdb_details_by_id(movie_id)
    return None



@st.cache_data(ttl=3600)
def tmdb_trailer_by_id(movie_id):
    """
    Fetch the first YouTube trailer for a movie.
    Returns a full YouTube URL or None.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=en-US"
    data = safe_request(url)
    if not data:
        return None

    for v in data.get("results", []):
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            key = v.get("key")
            if key:
                return f"https://www.youtube.com/watch?v={key}"

    return None


@st.cache_data(ttl=3600)
def tmdb_providers_by_id(movie_id, country="IN"):
    """
    Fetch streaming providers (Netflix, Prime, etc.) for a movie.
    Returns a sorted list of provider names.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"
    data = safe_request(url)
    if not data:
        return []

    results = data.get("results", {})
    country_info = results.get(country)
    if not country_info:
        return []

    providers = set()
    for key in ("flatrate", "buy", "rent"):
        for p in country_info.get(key, []) or []:
            name = p.get("provider_name")
            if name:
                providers.add(name)

    return sorted(providers)