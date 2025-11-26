# 🎬 CINEMATE – Movie & Film Recommendation Platform

Cinemate is a content-based movie recommendation system that suggests similar movies using TMDB datasets and cosine similarity.  
It processes movie metadata such as genres, cast, crew, overview, and keywords to recommend the most relevant films to the user.


## 🚀 Features

- Movie search functionality  
- Top similar movie recommendations  
- TMDB Movies & Credits dataset integrated  
- Cosine similarity–based ML model  
- Wishlist support  
- Clean and simple UI  

---

## 🧠 How It Works

1. TMDB datasets are loaded & merged  
2. Text-based features (overview, genres, cast, crew, keywords) are extracted  
3. A combined "tags" feature is created  
4. Similarity matrix generated using **Cosine Similarity**  
5. Recommendations shown based on similarity scores  

---

## 🛠 Tech Used

- **Python**  
- **pandas**, **numpy**  
- **scikit-learn**  
- **ast**, **requests**  
- **TMDB movie metadata**  

---

## 🖼 Screenshots

### 🏠 Home Page
![Home](Files/screenshots/Screenshot%202025-11-26%20200617.png)

### 🔍 Wishlist
![Wishlist](Files/screenshots/Screenshot%202025-11-26%20200020.png)

### 🎞 Recommendations Page
![Recommendations](Files/screenshots/Screenshot%202025-11-26%20200051.png)

### ⭐ Describe Movie
![Describe](Files/screenshots/Screenshot%202025-11-26%20200345.png)

### 💖 Trailer and Availability
![Trailer](Files/screenshots/Screenshot%202025-11-26%20200436.png)

### 📊 Compare Movies
![Compare](Files/screenshots/Screenshot%202025-11-26%20200725.png)

### 🖥 Final Compare Overview
![UI Overview](Files/screenshots/Screenshot%202025-11-26%20200743.png)

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
python main.py
