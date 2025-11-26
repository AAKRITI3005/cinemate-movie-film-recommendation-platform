import streamlit as st
from processing import preprocess as P

st.set_page_config(
    page_title="CineMate",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "wishlist" not in st.session_state:
    st.session_state["wishlist"] = P.load_wishlist()


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">

<style>
/* -------- Remove white header/footer -------- */
/* Ensure the page top is visible (prevent header clipping) */
section.main > div:first-child { padding-top: 0.5rem !important; }

/* Give the main block-container a safe top padding so the first line is not hidden
   Remove negative margin which causes the content to be pulled up under the header */
.block-container {
    padding-top: 3.2rem !important;   /* increase if still clipped (3.2rem -> 3.6rem -> 4rem) */
    margin-top: 0 !important;
}

/* Responsive tweak for narrow screens */
@media (max-width: 768px) {
    .block-container { padding-top: 4.2rem !important; }
}

/* -------- Global Background -------- */
body, .stApp {
    background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
    color: #f5f5f5;
    font-family: 'Poppins', sans-serif;
}

/* Sidebar Always Visible */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a0a, #161616);
    border-right: 3px solid #e50914;
    box-shadow: 0 0 25px rgba(229, 9, 20, 0.3);
}

/* Disable sidebar hide/collapse button */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Sidebar menu buttons */
div[role="radiogroup"] > label {
    background-color: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    padding: 10px 15px;
    margin-bottom: 10px;
    color: #f5f5f5 !important;
    font-weight: 600;
    font-size: 1.05rem;
    border: 1px solid rgba(255,255,255,0.1);
}
div[role="radiogroup"] > label:hover {
    border: 1px solid #e50914;
    transform: scale(1.03);
}
div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
    background: linear-gradient(90deg, #e50914, #b00610);
    color: #ffffff !important;
    transform: scale(1.05);
}


/* Remove sidebar title completely */
[data-testid="stSidebar"] h2 {
    display: none !important;
}

/* Sidebar radio options */
div[role="radiogroup"] > label {
    background-color: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    padding: 10px 15px;
    margin-bottom: 10px;
    color: #f5f5f5 !important;
    font-weight: 600;
    font-size: 1.05rem;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.1);
}
div[role="radiogroup"] > label:hover {
    border: 1px solid #e50914;
    color: #e50914 !important;
    transform: scale(1.03);
    box-shadow: 0 0 10px rgba(229,9,20,0.4);
}
div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
    background: linear-gradient(90deg, #e50914, #b00610);
    color: #ffffff !important;
    box-shadow: 0 0 15px rgba(229, 9, 20, 0.5);
    transform: scale(1.05);
}

/* -------- Input, Select, and Buttons -------- */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background-color: rgba(255,255,255,0.08) !important;
    color: #f5f5f5 !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.15);
    font-size: 1rem;
}
.stTextInput > label, .stSelectbox > label {
    color: #f5f5f5 !important;
    font-weight: 500;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #e50914, #b00610);
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 0.6rem 1.4rem;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 25px rgba(229,9,20,0.4);
}

/* -------- Movie Posters -------- */
img {
    border-radius: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
img:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(229,9,20,0.4);
}

.hero-section {
    text-align: center;
    padding: 3rem 1rem;
}
.hero-section h1 {
    font-size: 4rem;
    font-weight: 800;
    color: #ff1b1b;
    letter-spacing: 1px;
    text-shadow: 0 0 25px rgba(255, 0, 0, 0.6);
    margin-bottom: 0.5rem;
}
.hero-section h2 {
    font-size: 1.3rem;
    color: #cfcfcf;
    margin-bottom: 3rem;
    font-weight: 400;
}

/* -------- Info Card -------- */
.hero-box {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 2rem 1rem;
    box-shadow: 0 0 25px rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 2rem;
}
.hero-box p {
    font-size: 1.2rem;
    color: #f1f1f1;
}

/* -------- Section Titles -------- */
.section-title {
    color: #fff;
    font-size: 1.6rem;
    margin-top: 2rem;
    font-weight: 700;
}

/* -------- Footer -------- */
.footer {
    text-align: center;
    color: #aaa;
    margin-top: 2rem;
}
            /* Disable sidebar hide button */
[data-testid="collapsedControl"] {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)


def is_in_wishlist(movie_id: int) -> bool:
    return any(item.get("id") == movie_id for item in st.session_state["wishlist"])


def add_to_wishlist(movie_id: int, fallback_title=None, fallback_poster=None, fallback_rating=None):
    if movie_id is None:
        return
    if is_in_wishlist(movie_id):
        return

  
    details = P.tmdb_details_by_id(movie_id)
    if details:
        item = {
            "id": movie_id,
            "title": details.get("title") or fallback_title,
            "year": details.get("year"),
            "poster": details.get("poster") or fallback_poster,
            "rating": details.get("imdb") or fallback_rating,
            "genre": details.get("genre"),
        }
    else:
        item = {
            "id": movie_id,
            "title": fallback_title,
            "year": None,
            "poster": fallback_poster,
            "rating": fallback_rating,
            "genre": None,
        }

    st.session_state["wishlist"].append(item)
    P.save_wishlist(st.session_state["wishlist"])


def remove_from_wishlist(movie_id: int):
    st.session_state["wishlist"] = [
        item for item in st.session_state["wishlist"] if item.get("id") != movie_id
    ]
    P.save_wishlist(st.session_state["wishlist"])


def render_movie_card(info: dict, movie_id: int, col, context_key: str):
    """
    Helper to render a movie card with poster, title, rating, and heart.
    context_key makes button keys unique (e.g. 'home', 'popular', 'wish').
    """
    with col:
        poster = info.get("poster")
        title = info.get("title", "Unknown")
        year = info.get("year")
        rating = info.get("imdb") or info.get("rating")
        genre = info.get("genre")

        if poster:
            st.image(poster, use_container_width=True)
        if year:
            st.markdown(f"**{title} ({year})**")
        else:
            st.markdown(f"**{title}**")
        if rating is not None:
            st.caption(f"⭐ {rating}/10  |  {genre or ''}")
        elif genre:
            st.caption(genre)

        key = f"heart_{context_key}_{movie_id}"
        liked = is_in_wishlist(movie_id)
        label = "❤️" if liked else "🤍"

        if st.button(label, key=key):
            if liked:
                remove_from_wishlist(movie_id)
            else:
                add_to_wishlist(movie_id, fallback_title=title, fallback_poster=poster, fallback_rating=rating)


menu = ["Home", "Recommend Movies", "Compare Movies", "Describe a Movie", "Popular Movies", "Wishlist", "About"]

choice = st.sidebar.radio("Navigate", menu)



if choice == "Home":
    st.markdown("""
        <div class="hero-section">
            <h1>🎬 CineMate</h1>
            <h2>Discover, Explore & Enjoy Movies Like Never Before — powered by TMDb + OMDb APIs.</h2>
        </div>
        <div class="hero-box">
            <p>
                Personalized movie recommendations fetched in real-time.<br>
                Built for film lovers who crave endless discovery.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 class='section-title'>🔥 Trending Right Now</h3>", unsafe_allow_html=True)

    with st.spinner("Fetching trending movies..."):
        trending = P.tmdb_popular_titles(pages=2)

    if trending:
        movie_cards = []
        for m in trending[:10]:
            info = P.tmdb_details_by_id(m["id"])
            if info:
                # attach id inside info for safety
                info["id"] = m["id"]
                movie_cards.append(info)

        cols = st.columns(5)
        for i, m in enumerate(movie_cards):
            col = cols[i % 5]
            render_movie_card(m, m["id"], col, context_key="home")
    else:
        st.warning("Couldn't load trending movies. Try again later!")

    st.markdown("<div class='footer'>Made with ❤️ by <b>Swastik Sharma</b></div>", unsafe_allow_html=True)


elif choice == "Recommend Movies":
    st.subheader("Recommend Me a Similar Movie")

    q = st.text_input("Search a movie (title):", "")
    colA, colB = st.columns([3, 1])
    with colA:
        options = P.tmdb_search(q, max_pages=2) if q.strip() else P.tmdb_popular_titles(pages=3)
    with colB:
        st.caption("")

    labels = [o["label"] for o in options] if options else []
    selected_label = st.selectbox("Select a movie...", labels, index=0 if labels else None)

    selected_id = next((o["id"] for o in options if o["label"] == selected_label), None) if selected_label else None

    if st.button("Recommend"):
        if not selected_id:
            st.warning("Please search and select a movie.")
        else:
            with st.spinner("Fetching live recommendations..."):
                recs = P.tmdb_similar_by_id(selected_id)
            if not recs:
                st.warning("No similar movies found. Try another title.")
            else:
                st.subheader("Best Recommendations (Live Data)")
                cols = st.columns(5)
                for i, m in enumerate(recs):
                    col = cols[i % 5]
                    with col:
                        poster = m.get("poster")
                        title = m.get("title")
                        rating = m.get("rating")
                        movie_id = m.get("id")

                        if poster:
                            st.image(poster, use_container_width=True)
                        st.markdown(f"**{title}**")
                        if rating is not None:
                            st.caption(f"Rating: {rating}")

                        liked = is_in_wishlist(movie_id)
                        label = "❤️" if liked else "🤍"
                        key = f"heart_rec_{movie_id}"
                        if st.button(label, key=key):
                            if liked:
                                remove_from_wishlist(movie_id)
                            else:
                                add_to_wishlist(
                                    movie_id,
                                    fallback_title=title,
                                    fallback_poster=poster,
                                    fallback_rating=rating,
                                )

# =====================================================
# 🔁 COMPARE MOVIES
# =====================================================
elif choice == "Compare Movies":
    st.subheader("Compare Two Movies — Side by Side")

    # Search inputs (type-to-search)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        q1 = st.text_input("Search movie 1 (title):", key="cmp_q1")
        opts1 = P.tmdb_search(q1, max_pages=2) if q1.strip() else P.tmdb_popular_titles(pages=2)
        labels1 = [o["label"] for o in opts1] if opts1 else []
        sel1 = st.selectbox("Select movie 1...", labels1, index=0 if labels1 else None, key="cmp_sel1")
    with col_s2:
        q2 = st.text_input("Search movie 2 (title):", key="cmp_q2")
        opts2 = P.tmdb_search(q2, max_pages=2) if q2.strip() else P.tmdb_popular_titles(pages=2)
        labels2 = [o["label"] for o in opts2] if opts2 else []
        sel2 = st.selectbox("Select movie 2...", labels2, index=0 if labels2 else None, key="cmp_sel2")

    id1 = next((o["id"] for o in opts1 if o["label"] == sel1), None) if sel1 else None
    id2 = next((o["id"] for o in opts2 if o["label"] == sel2), None) if sel2 else None

    # Compare button
    if st.button("Compare"):
        if not id1 or not id2:
            st.warning("Please select both movies to compare.")
        elif id1 == id2:
            st.info("You selected the same movie twice — try two different movies.")
        else:
            with st.spinner("Fetching details..."):
                info1 = P.tmdb_details_by_id(id1)
                info2 = P.tmdb_details_by_id(id2)

            if not info1 or not info2:
                st.error("Couldn't fetch details for one or both movies. Try again.")
            else:
                # Side-by-side posters + title
                left, right = st.columns([1,1])
                with left:
                    if info1.get("poster"):
                        st.image(info1["poster"], use_container_width=True)
                    st.markdown(f"### {info1.get('title','-')} ({info1.get('year','-')})")
                    st.markdown(f"**Genre:** {info1.get('genre','-')}")
                    st.markdown(f"**Rating:** {info1.get('imdb','-')}")
                    st.markdown("**Overview:**")
                    st.write(info1.get("plot","-"))
                
                    tr1 = P.tmdb_trailer_by_id(id1)
                    if tr1:
                        st.markdown(f"[Watch Trailer]({tr1})")
                   
                    prov1 = P.tmdb_providers_by_id(id1, country="IN")
                    if prov1:
                        st.markdown("**Available on:** " + ", ".join(prov1))
                  
                    liked1 = is_in_wishlist(id1)
                    if st.button("❤️ Remove from Wishlist" if liked1 else "🤍 Add to Wishlist", key=f"cmp_wish_{id1}"):
                        if liked1:
                            remove_from_wishlist(id1)
                        else:
                            add_to_wishlist(id1, fallback_title=info1.get("title"), fallback_poster=info1.get("poster"), fallback_rating=info1.get("imdb"))

                with right:
                    if info2.get("poster"):
                        st.image(info2["poster"], use_container_width=True)
                    st.markdown(f"### {info2.get('title','-')} ({info2.get('year','-')})")
                    st.markdown(f"**Genre:** {info2.get('genre','-')}")
                    st.markdown(f"**Rating:** {info2.get('imdb','-')}")
                    st.markdown("**Overview:**")
                    st.write(info2.get("plot","-"))
                    tr2 = P.tmdb_trailer_by_id(id2)
                    if tr2:
                        st.markdown(f"[Watch Trailer]({tr2})")
                    prov2 = P.tmdb_providers_by_id(id2, country="IN")
                    if prov2:
                        st.markdown("**Available on:** " + ", ".join(prov2))
                    liked2 = is_in_wishlist(id2)
                    if st.button("❤️ Remove from Wishlist" if liked2 else "🤍 Add to Wishlist", key=f"cmp_wish_{id2}"):
                        if liked2:
                            remove_from_wishlist(id2)
                        else:
                            add_to_wishlist(id2, fallback_title=info2.get("title"), fallback_poster=info2.get("poster"), fallback_rating=info2.get("imdb"))

               
                st.markdown("---")
                st.markdown("### Quick Comparison")
                comp_cols = st.columns([1,1,1])
                with comp_cols[0]:
                    st.write("Attribute")
                    st.write("Title")
                    st.write("Year")
                    st.write("Genre")
                    st.write("Rating")
                with comp_cols[1]:
                    st.write("Movie 1")
                    st.write(info1.get("title","-"))
                    st.write(info1.get("year","-"))
                    st.write(info1.get("genre","-"))
                    st.write(info1.get("imdb","-"))
                with comp_cols[2]:
                    st.write("Movie 2")
                    st.write(info2.get("title","-"))
                    st.write(info2.get("year","-"))
                    st.write(info2.get("genre","-"))
                    st.write(info2.get("imdb","-"))

elif choice == "Describe a Movie":
    st.subheader("Describe Me a Movie")

    title = st.text_input("Enter the name of a movie:")
    if st.button("Describe"):
        if not title.strip():
            st.warning("Please enter a movie name.")
        else:
            with st.spinner("Fetching details..."):
                info = P.describe_movie(title)
            if not info:
                st.error("Couldn't find details. Try another movie.")
            else:
              
                movie_id = P.tmdb_id_for_title(info.get("title", title))

                if info.get("poster"):
                    st.image(info["poster"], width=300)
                st.markdown(f"**Title:** {info.get('title','-')} ({info.get('year','-')})")
                st.markdown(f"**Genre:** {info.get('genre','-')}")
                st.markdown(f"**Director:** {info.get('director','-')}")
                st.markdown(f"**Actors:** {info.get('actors','-')}")
                st.markdown(f"**Rating:** {info.get('imdb','-')}")
                st.markdown("**Overview:**")
                st.write(info.get("plot","-"))

                # Wishlist heart for this movie
                if movie_id:
                    liked = is_in_wishlist(movie_id)
                    label = "❤️ Remove from Wishlist" if liked else "🤍 Add to Wishlist"
                    if st.button(label, key=f"heart_describe_{movie_id}"):
                        if liked:
                            remove_from_wishlist(movie_id)
                        else:
                            add_to_wishlist(
                                movie_id,
                                fallback_title=info.get("title"),
                                fallback_poster=info.get("poster"),
                                fallback_rating=info.get("imdb"),
                            )

                # Trailer + Where to watch
                if movie_id:
                    st.markdown("---")
                    st.markdown("### 🎞 Trailer & Availability")

                    trailer_url = P.tmdb_trailer_by_id(movie_id)
                    providers = P.tmdb_providers_by_id(movie_id, country="IN")

                    if trailer_url:
                        st.markdown("**Watch Trailer:**")
                        st.video(trailer_url)
                    else:
                        st.info("Trailer not available for this title.")

                    if providers:
                        st.markdown("**Available On:** " + ", ".join(providers))
                    else:
                        st.markdown("**Available On:** Not available in provider data for your region.")
                else:
                    st.info("Additional streaming/trailer information is not available for this title.")



elif choice == "Popular Movies":
    st.subheader("Popular Movies (Live)")

    with st.spinner("Loading popular movies..."):
        popular = P.tmdb_popular_titles(pages=5)

    if not popular:
        st.warning("Couldn't fetch popular movies at the moment.")
    else:
        st.caption(f"Showing {len(popular)} trending movies right now 🔥")
        movie_cards = []
        for m in popular[:40]:
            info = P.tmdb_details_by_id(m["id"])
            if info:
                info["id"] = m["id"]
                movie_cards.append(info)

        cols = st.columns(5)
        for i, m in enumerate(movie_cards):
            col = cols[i % 5]
            render_movie_card(m, m["id"], col, context_key="popular")



elif choice == "Wishlist":
    st.subheader("❤️ My Wishlist")

    wishlist = st.session_state["wishlist"]
    if not wishlist:
        st.info("Your wishlist is empty. Go like some movies first!")
    else:
        cols = st.columns(5)
        for i, item in enumerate(wishlist):
            col = cols[i % 5]
            # For wishlist, info is already stored
            info = {
                "title": item.get("title"),
                "year": item.get("year"),
                "poster": item.get("poster"),
                "imdb": item.get("rating"),
                "genre": item.get("genre"),
            }
            render_movie_card(info, item["id"], col, context_key="wishlist")



elif choice == "About":
    st.markdown("""
        <div class="hero-section">
            <h1>About CineMate</h1>
            <h2>Dynamic, API-Powered, and Built for Movie Enthusiasts</h2>
        </div>

        <div class="hero-box">
            <p>
                A sleek and smart platform built using <b>Python</b> and <b>Streamlit</b>,
                integrating <b>TMDb</b> and <b>OMDb</b> APIs to fetch live movie data,
                descriptions, recommendations, trailers, and streaming availability. 
            </p>
            <br>
            <p><b>Tech Stack:</b> Python · Streamlit · TMDb API · OMDb API</p>
            <br>
            <i>“Turning data into cinematic experiences.”</i><br><br>
            Made with ❤️ by <b>Aakriti Srivastava</b>
        </div>
    """, unsafe_allow_html=True)