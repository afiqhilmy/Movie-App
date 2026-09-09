import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

# -----------------------------------------------------------------------------
# 1. STREAMLIT CONFIG & CUSTOM CSS (GSC BRANDING & WATERMARKS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Itspeak cinema | Peak Film Vault",
    page_icon="🎬",
    layout="wide"
)

# Custom Styling Injection
st.markdown("""
<style>
    /* Global Font Enforcement */
    * {
        font-family: 'Trebuchet MS', 'Segoe UI', 'Arial', sans-serif !important;
    }

    /* Main App Background */
    .stApp {
        background-color: #0d0d0d;
        color: #FFFFFF;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #141414 !important;
        border-right: 1px solid #2a2a2a;
    }

    /* Header Watermark */
    .header-watermark {
        text-align: center;
        font-size: 0.85rem;
        letter-spacing: 2.5px;
        color: #FFC72C;
        text-shadow: 0px 0px 8px rgba(255, 199, 44, 0.5);
        padding: 8px 15px;
        background: #121212;
        border: 1px solid #2a2a2a;
        margin-bottom: 20px;
        font-weight: 700;
        text-transform: uppercase;
        border-radius: 6px;
    }

    /* Footer Watermark */
    .footer-watermark {
        text-align: center;
        font-size: 0.9rem;
        color: #AAAAAA;
        padding: 20px 0;
        letter-spacing: 1.5px;
    }
    .footer-watermark a {
        color: #FFC72C;
        text-decoration: none;
        font-weight: bold;
    }
    .footer-watermark a:hover {
        text-decoration: underline;
        color: #FFE082;
    }

    /* Top Header Bar Styling */
    .gsc-header {
        background: linear-gradient(180deg, #181818 0%, #0d0d0d 100%);
        padding: 28px;
        border-radius: 12px;
        border: 1px solid #FFC72C;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.7);
    }

    .gsc-title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }

    .gsc-title {
        color: #FFC72C !important;
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        letter-spacing: 4px;
        text-shadow: 0px 0px 18px rgba(255, 199, 44, 0.6);
        margin: 0;
        text-transform: uppercase;
    }

    .gsc-subtitle {
        color: #E0E0E0;
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 10px;
        letter-spacing: 1px;
    }

    /* Movie Card Container & Layout */
    .movie-card {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
        transition: transform 0.2s, border-color 0.2s;
    }
    
    .movie-card:hover {
        border-color: #FFC72C;
        transform: translateY(-3px);
    }

    .poster-wrapper {
        position: relative;
        width: 100%;
        margin-bottom: 8px;
    }

    .poster-img {
        width: 100%;
        height: 380px;
        object-fit: cover;
        border-radius: 6px;
        image-rendering: -webkit-optimize-contrast;
        display: block;
    }

    /* Rank Badge Overlay on Poster */
    .rank-badge {
        position: absolute;
        top: 8px;
        left: 8px;
        background-color: #FFC72C;
        color: #0d0d0d;
        font-weight: 900;
        font-size: 0.9rem;
        padding: 4px 9px;
        border-radius: 4px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.8);
        z-index: 10;
    }

    .movie-title-gold {
        color: #FFC72C;
        font-weight: 800;
        font-size: 1.25rem;
        margin-top: 6px;
        margin-bottom: 4px;
        line-height: 1.25;
    }

    .movie-meta-info {
        color: #CCCCCC;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /* Button Styling for Movie Container */
    div.stButton > button {
        background-color: #161616;
        color: #FFC72C;
        border: 1px solid #FFC72C;
        border-radius: 6px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        white-space: normal !important;
        word-wrap: break-word !important;
        height: auto !important;
        min-height: 42px;
        padding: 8px 12px;
    }

    div.stButton > button:hover {
        background-color: #FFC72C;
        color: #0d0d0d;
        border-color: #FFC72C;
        box-shadow: 0px 0px 12px rgba(255, 199, 44, 0.6);
    }

    /* Filter Box Styling */
    .filter-container {
        background-color: #141414;
        border: 1px solid #2a2a2a;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }

/* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border-radius: 6px 6px 0px 0px;
        border: 1px solid #2a2a2a;
        padding: 10px 28px !important; /* Increased side padding */
    }

    .stTabs [data-baseweb="tab"] p {
        padding: 0 6px !important; /* Gives text horizontal breathing space */
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFC72C !important;
        color: #000000 !important;
        font-weight: bold;
    }

    /* 1. Multiselect tag background & text */
    span[data-baseweb="tag"] {
        background-color: #FFC72C !important;
        color: #000000 !important;
    }

    /* 2. Slider fill track color */
    div[data-baseweb="slider"] div[aria-hidden="true"] > div {
        background-color: #FFC72C !important;
    }

    /* 3. Slider handle (circle) color */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #FFC72C !important;
        border-color: #FFC72C !important;
    }

    /* 4. Slider value text numbers (e.g., 1930, 2019, 7.50) */
    div[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
        color: #FFC72C !important;
    }



    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PLOTLY THEME CONFIGURATION
# -----------------------------------------------------------------------------
GOLD_COLOR = "#FFC72C"

def apply_plotly_theme(fig, height=340):
    """Applies a sleek dark cinematic gold theme to Plotly charts."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(20,20,20,0.6)",
        font=dict(family="Trebuchet MS, Segoe UI, sans-serif", color="#CCCCCC"),
        title=dict(font=dict(color=GOLD_COLOR, size=15)),
        margin=dict(l=40, r=20, t=45, b=40),
        height=height,
        xaxis=dict(gridcolor="#222222", zerolinecolor="#333333"),
        yaxis=dict(gridcolor="#222222", zerolinecolor="#333333"),
        legend=dict(
            font=dict(color="#CCCCCC"),
            title=dict(font=dict(color=GOLD_COLOR)),
            bgcolor="rgba(20,20,20,0.8)",
            bordercolor="#2a2a2a",
            borderwidth=1
        )
    )
    return fig

# -----------------------------------------------------------------------------
# 3. DATA LOADING PIPELINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("imdb_cleaned_data.csv")
    
    def upgrade_poster_quality(url):
        if pd.isna(url):
            return "https://via.placeholder.com/600x900?text=No+Poster+Available"
        return re.sub(r'\._V1_.*?\.', '.', str(url))

    df['Poster_Link'] = df['Poster_Link'].apply(upgrade_poster_quality)
    
    # Cleaning Numeric Columns
    df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
    df['Runtime_Min'] = df['Runtime'].astype(str).str.replace(' min', '').str.extract(r'(\d+)').astype(float)
    df['Gross_Clean'] = df['Gross'].astype(str).str.replace(',', '').str.extract(r'(\d+)').astype(float)
    df['IMDB_Rating'] = pd.to_numeric(df['IMDB_Rating'], errors='coerce')
    df['Meta_score'] = pd.to_numeric(df['Meta_score'], errors='coerce')
    df['No_of_Votes'] = pd.to_numeric(df['No_of_Votes'], errors='coerce')
    
    # Rank Assignment (1 to N based on IMDb Dataset Ordering)
    df['Rank'] = np.arange(1, len(df) + 1)
    
    # Extract unique genres
    genres_set = set()
    for g in df['Genre'].dropna():
        for item in g.split(','):
            genres_set.add(item.strip())
            
    df['Decade'] = (df['Released_Year'] // 10 * 10).astype('Int64').astype(str) + 's'
    
    return df, sorted(list(genres_set))

df, all_genres = load_data()

# Session State Initialization
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = set()
if 'selected_movie_idx' not in st.session_state:
    st.session_state.selected_movie_idx = None
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "🎬 Movie Catalog"

# -----------------------------------------------------------------------------
# 4. HEADER WATERMARK
# -----------------------------------------------------------------------------
st.markdown('<div class="header-watermark">MOVIE APP BY AFIQ HILMY | DATA ANALYTICS | MOVIE ENTHUSIAST</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#FFC72C; text-align:center;'>ITS PEAK CINEMA</h2>", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "Navigate", 
    ["🎬 Movie Catalog", "❤️ My List & Watchlist", "📊 Analytics Dashboard"],
    index=["🎬 Movie Catalog", "❤️ My List & Watchlist", "📊 Analytics Dashboard"].index(st.session_state.current_tab) 
    if st.session_state.current_tab in ["🎬 Movie Catalog", "❤️ My List & Watchlist", "📊 Analytics Dashboard"] else 0
)

st.session_state.current_tab = nav_selection

# -----------------------------------------------------------------------------
# PAGE 1: MOVIE CATALOG & DETAIL VIEW
# -----------------------------------------------------------------------------
if st.session_state.current_tab == "🎬 Movie Catalog":
    
    # Detailed Movie View
    if st.session_state.selected_movie_idx is not None:
        movie = df.iloc[st.session_state.selected_movie_idx]
        
        if st.button("⬅️ Back to Catalog"):
            st.session_state.selected_movie_idx = None
            st.rerun()
            
        st.markdown("<hr style='border: 1px solid #FFC72C;'>", unsafe_allow_html=True)
        
        col_poster, col_info = st.columns([1, 2])
        
        with col_poster:
            st.image(movie['Poster_Link'], use_container_width=True)
            
            movie_title = movie['Series_Title']
            col_b1, col_b2 = st.columns(2)
            
            with col_b1:
                is_fav = movie_title in st.session_state.favorites
                btn_fav_label = "❤️ Liked" if is_fav else "🤍 Like"
                if st.button(btn_fav_label, key=f"det_fav_{movie_title}"):
                    if is_fav:
                        st.session_state.favorites.remove(movie_title)
                    else:
                        st.session_state.favorites.add(movie_title)
                    st.rerun()
                    
            with col_b2:
                is_watch = movie_title in st.session_state.watchlist
                btn_watch_label = "🔖 Saved" if is_watch else "➕ Watchlist"
                if st.button(btn_watch_label, key=f"det_watch_{movie_title}"):
                    if is_watch:
                        st.session_state.watchlist.remove(movie_title)
                    else:
                        st.session_state.watchlist.add(movie_title)
                    st.rerun()

        with col_info:
            # Display Rank along with Title in details view
            st.markdown(f"<h1 style='color:#FFC72C;'>#{movie['Rank']} - {movie['Series_Title']}</h1>", unsafe_allow_html=True)
            st.markdown(f"**Year:** {int(movie['Released_Year']) if pd.notnull(movie['Released_Year']) else 'N/A'} | "
                        f"**Certificate:** {movie['Certificate']} | "
                        f"**Runtime:** {movie['Runtime']}")
            st.markdown(f"**Genre:** {movie['Genre']}")
            
            st.markdown("---")
            
            m0, m1, m2, m3, m4 = st.columns(5)
            m0.metric("IMDb Rank", f"#{movie['Rank']}")
            m1.metric("IMDb Rating", f"⭐ {movie['IMDB_Rating']}")
            m2.metric("Metascore", f"🎯 {movie['Meta_score'] if pd.notnull(movie['Meta_score']) else 'N/A'}")
            m3.metric("Total Votes", f"👥 {int(movie['No_of_Votes']):,}" if pd.notnull(movie['No_of_Votes']) else "N/A")
            m4.metric("Gross Revenue", f"💵 ${movie['Gross_Clean']:,.0f}" if pd.notnull(movie['Gross_Clean']) else "N/A")
            
            st.markdown("---")
            st.subheader("Overview & Synopsis")
            st.write(movie['Overview'])
            
            st.subheader("Cast & Crew")
            st.markdown(f"**Director:** {movie['Director']}")
            st.markdown(f"**Starring:** {movie['Star1']}, {movie['Star2']}, {movie['Star3']}, {movie['Star4']}")
            
    else:
        # Header Bar
        st.markdown("""
        <div class="gsc-header">
            <div class="gsc-title-container">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FFC72C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0px 0px 10px #FFC72C);">
                    <path d="M19.82 2H4.18C2.97 2 2 2.97 2 4.18v15.64C2 21.03 2.97 22 4.18 22h15.64c1.21 0 2.18-.97 2.18-2.18V4.18C22 2.97 21.03 2 19.82 2z"></path>
                    <path d="M7 2v20M17 2v20M2 12h20M2 7h5M2 17h5M17 17h5M17 7h5"></path>
                </svg>
                <h1 class="gsc-title">IT'S PEAK CINEMA</h1>
            </div>
            <div class="gsc-subtitle">Discover peak cinema & top tier films from the IMDB top movies ranking</div>
        </div>
        """, unsafe_allow_html=True)
        
        # REQUIREMENT 1: DIRECT FILTER SECTION WITH SORTING CONTROL
        st.markdown("### 🍿 Find a movie")
        
        search_query = st.text_input("🔍 Search Movies by Title, Director, or Actor", "")
        
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
        
        with f_col1:
            selected_genres = st.multiselect("Filter by Genre", options=all_genres)
        
        with f_col2:
            min_year, max_year = int(df['Released_Year'].min()), int(df['Released_Year'].max())
            year_range = st.slider("Release Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))
        
        with f_col3:
            rating_cutoff = st.slider("Minimum IMDb Rating", min_value=7.0, max_value=10.0, value=7.5, step=0.1)
            
        with f_col4:
            certificates = sorted([str(x) for x in df['Certificate'].dropna().unique()])
            selected_certs = st.multiselect("Certificate / Age Rating", options=certificates)

        with f_col5:
            sort_option = st.selectbox(
                "Sort Movies By",
                options=[
                    "Rank (Default)",
                    "Release Year: Newest First",
                    "Release Year: Oldest First",
                    "Duration: Longest First",
                    "Duration: Shortest First",
                    "IMDb Rating: Highest First"
                ]
            )

        # Filter Logic
        filtered_df = df.copy()
        
        if search_query:
            q = search_query.lower()
            filtered_df = filtered_df[
                filtered_df['Series_Title'].astype(str).str.lower().str.contains(q) |
                filtered_df['Director'].astype(str).str.lower().str.contains(q) |
                filtered_df['Star1'].astype(str).str.lower().str.contains(q) |
                filtered_df['Star2'].astype(str).str.lower().str.contains(q)
            ]
            
        if selected_genres:
            filtered_df = filtered_df[filtered_df['Genre'].apply(lambda g: any(genre in str(g) for genre in selected_genres))]
            
        filtered_df = filtered_df[
            (filtered_df['Released_Year'] >= year_range[0]) & 
            (filtered_df['Released_Year'] <= year_range[1]) &
            (filtered_df['IMDB_Rating'] >= rating_cutoff)
        ]
        
        if selected_certs:
            filtered_df = filtered_df[filtered_df['Certificate'].isin(selected_certs)]

        # Sorting Logic
        if sort_option == "Release Year: Newest First":
            filtered_df = filtered_df.sort_values(by="Released_Year", ascending=False)
        elif sort_option == "Release Year: Oldest First":
            filtered_df = filtered_df.sort_values(by="Released_Year", ascending=True)
        elif sort_option == "Duration: Longest First":
            filtered_df = filtered_df.sort_values(by="Runtime_Min", ascending=False)
        elif sort_option == "Duration: Shortest First":
            filtered_df = filtered_df.sort_values(by="Runtime_Min", ascending=True)
        elif sort_option == "IMDb Rating: Highest First":
            filtered_df = filtered_df.sort_values(by="IMDB_Rating", ascending=False)
        else:
            filtered_df = filtered_df.sort_values(by="Rank", ascending=True)

        st.markdown(f"<p style='color:#FFC72C; font-size:1.1rem; font-weight:bold; margin-top:15px;'>Showing <b>{len(filtered_df)}</b> films matching your filters</p>", unsafe_allow_html=True)

        # REQUIREMENT 2 & 3: MOVIE CARD LAYOUT WITH CORNER RANKING BADGE AND CLICKABLE DETAILS BUTTON
        cols_per_row = 4
        cols = st.columns(cols_per_row)
        
        for idx, (original_idx, row) in enumerate(filtered_df.iterrows()):
            col = cols[idx % cols_per_row]
            with col:
                st.markdown(f"""
                <div class="movie-card">
                    <div class="poster-wrapper">
                        <span class="rank-badge">#{row['Rank']}</span>
                        <img src="{row['Poster_Link']}" class="poster-img">
                    </div>
                    <div class="movie-title-gold">{row['Series_Title']}</div>
                    <div class="movie-meta-info">{int(row['Released_Year']) if pd.notnull(row['Released_Year']) else 'N/A'} &nbsp;|&nbsp; ⭐ {row['IMDB_Rating']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("View Details", key=f"det_btn_{original_idx}", use_container_width=True):
                    st.session_state.selected_movie_idx = original_idx
                    st.rerun()

# -----------------------------------------------------------------------------
# PAGE 2: FAVORITES AND WATCHLIST
# -----------------------------------------------------------------------------
elif st.session_state.current_tab == "❤️ My List & Watchlist":
    st.markdown("""
    <div class="gsc-header">
        <h1 class="gsc-title">YOUR PERSONAL COLLECTION</h1>
        <div class="gsc-subtitle">Manage your favorite films and upcoming cinema watchlist</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab_fav, tab_watch = st.tabs(["❤️ Favorites", "🔖 Watchlist"])
    
    with tab_fav:
        if not st.session_state.favorites:
            st.info("You haven't added any movies to your favorites yet! Browse the catalog and click '🤍 Like'.")
        else:
            fav_df = df[df['Series_Title'].isin(st.session_state.favorites)]
            cols = st.columns(4)
            for idx, (original_idx, row) in enumerate(fav_df.iterrows()):
                with cols[idx % 4]:
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="poster-wrapper">
                            <span class="rank-badge">#{row['Rank']}</span>
                            <img src="{row['Poster_Link']}" class="poster-img">
                        </div>
                        <div class="movie-title-gold">{row['Series_Title']}</div>
                        <div class="movie-meta-info">{int(row['Released_Year'])} &nbsp;|&nbsp; ⭐ {row['IMDB_Rating']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Remove ❤️", key=f"rem_fav_{original_idx}"):
                        st.session_state.favorites.remove(row['Series_Title'])
                        st.rerun()

    with tab_watch:
        if not st.session_state.watchlist:
            st.info("Your watchlist is empty! Browse the catalog and click '➕ Watchlist' to save movies.")
        else:
            watch_df = df[df['Series_Title'].isin(st.session_state.watchlist)]
            cols = st.columns(4)
            for idx, (original_idx, row) in enumerate(watch_df.iterrows()):
                with cols[idx % 4]:
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="poster-wrapper">
                            <span class="rank-badge">#{row['Rank']}</span>
                            <img src="{row['Poster_Link']}" class="poster-img">
                        </div>
                        <div class="movie-title-gold">{row['Series_Title']}</div>
                        <div class="movie-meta-info">{int(row['Released_Year'])} &nbsp;|&nbsp; ⭐ {row['IMDB_Rating']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Remove 🔖", key=f"rem_watch_{original_idx}"):
                        st.session_state.watchlist.remove(row['Series_Title'])
                        st.rerun()

# -----------------------------------------------------------------------------
# PAGE 3: ANALYTICS DASHBOARD (REQUIREMENT 4: PLOTLY LIBRARY)
# -----------------------------------------------------------------------------
elif st.session_state.current_tab == "📊 Analytics Dashboard":
    st.markdown("""
    <div class="gsc-header">
        <h1 class="gsc-title">MOVIES DASHBOARD AND STORY</h1>
        <div class="gsc-subtitle">4 Key Stories across the IMDb Top dataset, featuring 20 interactive Plotly visualizations</div>
    </div>
    """, unsafe_allow_html=True)
    
    story1, story2, story3, story4 = st.tabs([
        "📜 Story 1: Golden Era & Evolution",
        "💰 Story 2: Box Office & Financials",
        "🎬 Story 3: Directors & Star Power",
        "🎭 Story 4: Genre Spectrum & Ratings"
    ])
    
    # STORY 1: Golden Era & Evolution
    with story1:
        st.subheader("Story 1: Golden Era & Evolution of Cinema")
        c1, c2 = st.columns(2)
        
        with c1:
            # 1. Movies per Decade
            decade_counts = df['Decade'].dropna().value_counts().reset_index()
            decade_counts.columns = ['Decade', 'Count']
            decade_counts = decade_counts.sort_values('Decade')
            
            fig1 = px.bar(decade_counts, x='Decade', y='Count', title="1. Top Movies Released per Decade", color_discrete_sequence=[GOLD_COLOR])
            fig1.update_traces(hovertemplate="<b>Decade:</b> %{x}<br><b>Count:</b> %{y}")
            st.plotly_chart(apply_plotly_theme(fig1), use_container_width=True)
            
            # 2. Average IMDb Rating Trend
            decade_rating = df.groupby('Decade')['IMDB_Rating'].mean().reset_index().sort_values('Decade')
            
            fig2 = px.line(decade_rating, x='Decade', y='IMDB_Rating', markers=True, title="2. Average IMDb Rating Trend Across Decades", color_discrete_sequence=[GOLD_COLOR])
            fig2.update_traces(hovertemplate="<b>Decade:</b> %{x}<br><b>Avg Rating:</b> %{y:.2f}")
            fig2.update_yaxes(range=[7.5, 8.5], title="Avg IMDb Rating")
            st.plotly_chart(apply_plotly_theme(fig2), use_container_width=True)

        with c2:
            # 3. Certificate Distribution
            cert_counts = df['Certificate'].fillna('Unrated').value_counts().head(7).reset_index()
            cert_counts.columns = ['Certificate', 'Count']
            
            fig3 = px.bar(cert_counts, x='Count', y='Certificate', orientation='h', title="3. Content Certificate Distribution", color_discrete_sequence=[GOLD_COLOR])
            fig3.update_layout(yaxis=dict(autorange="reversed", title="Age Certificate"), xaxis=dict(title="Movie Count"))
            fig3.update_traces(hovertemplate="<b>Certificate:</b> %{y}<br><b>Count:</b> %{x}")
            st.plotly_chart(apply_plotly_theme(fig3), use_container_width=True)
            
            # 4. Average Movie Runtime
            runtime_decade = df.groupby('Decade')['Runtime_Min'].mean().reset_index().dropna().sort_values('Decade')
            
            fig4 = px.area(runtime_decade, x='Decade', y='Runtime_Min', title="4. Average Movie Runtime (Minutes) Over Time", color_discrete_sequence=[GOLD_COLOR])
            fig4.update_traces(hovertemplate="<b>Decade:</b> %{x}<br><b>Avg Runtime:</b> %{y:.1f} min")
            fig4.update_yaxes(title="Avg Runtime (Min)")
            st.plotly_chart(apply_plotly_theme(fig4), use_container_width=True)
            
        # 5. Cumulative Fan Votes
        votes_decade = df.groupby('Decade')['No_of_Votes'].sum().reset_index().dropna().sort_values('Decade')
        fig5 = px.bar(votes_decade, x='Decade', y='No_of_Votes', title="5. Cumulative Fan Votes per Decade", color_discrete_sequence=[GOLD_COLOR])
        fig5.update_traces(hovertemplate="<b>Decade:</b> %{x}<br><b>Total Votes:</b> %{y:,}")
        fig5.update_yaxes(title="Total IMDb Votes")
        st.plotly_chart(apply_plotly_theme(fig5, height=360), use_container_width=True)

    # STORY 2: Box Office & Financials
    with story2:
        st.subheader("Story 2: Box Office Titans & Financial Dynamics")
        c1, c2 = st.columns(2)
        
        with c1:
            # 6. Top 10 Highest Grossing Movies
            top_gross = df.dropna(subset=['Gross_Clean']).nlargest(10, 'Gross_Clean')
            fig6 = px.bar(top_gross, x='Gross_Clean', y='Series_Title', orientation='h', title="6. Top 10 Highest Grossing Movies ($)", color_discrete_sequence=[GOLD_COLOR], hover_data=['Released_Year'])
            fig6.update_layout(yaxis=dict(autorange="reversed", title="Film Title"), xaxis=dict(title="Gross Revenue ($)"))
            fig6.update_traces(hovertemplate="<b>%{y}</b><br>Gross Revenue: $%{x:,.0f}")
            st.plotly_chart(apply_plotly_theme(fig6), use_container_width=True)
            
            # 7. Rating vs Box Office Gross
            df_gross = df.dropna(subset=['Gross_Clean', 'IMDB_Rating'])
            fig7 = px.scatter(df_gross, x='IMDB_Rating', y='Gross_Clean', hover_name='Series_Title', title="7. IMDb Rating vs. Box Office Gross ($)", color_discrete_sequence=[GOLD_COLOR])
            fig7.update_traces(marker=dict(size=8, opacity=0.8), hovertemplate="<b>%{hovertext}</b><br>Rating: %{x}<br>Gross: $%{y:,.0f}")
            fig7.update_xaxes(range=[7.4, 9.5], title="IMDb Rating")
            fig7.update_yaxes(title="Gross Revenue ($)")
            st.plotly_chart(apply_plotly_theme(fig7), use_container_width=True)

        with c2:
            # 8. Votes Volume vs. Gross Earnings
            df_votes_gross = df.dropna(subset=['Gross_Clean', 'No_of_Votes', 'IMDB_Rating'])
            fig8 = px.scatter(df_votes_gross, x='No_of_Votes', y='Gross_Clean', size='IMDB_Rating', hover_name='Series_Title', title="8. Votes Volume vs. Gross Earnings", color_discrete_sequence=[GOLD_COLOR])
            fig8.update_traces(opacity=0.7, hovertemplate="<b>%{hovertext}</b><br>Votes: %{x:,}<br>Gross: $%{y:,.0f}")
            fig8.update_xaxes(title="Total Votes")
            fig8.update_yaxes(title="Gross Revenue ($)")
            st.plotly_chart(apply_plotly_theme(fig8), use_container_width=True)
            
            # 9. Metascore vs. Gross Revenue
            df_meta_gross = df.dropna(subset=['Gross_Clean', 'Meta_score'])
            fig9 = px.scatter(df_meta_gross, x='Meta_score', y='Gross_Clean', hover_name='Series_Title', title="9. Metascore vs. Gross Revenue", color_discrete_sequence=[GOLD_COLOR])
            fig9.update_traces(marker=dict(size=7, opacity=0.8), hovertemplate="<b>%{hovertext}</b><br>Metascore: %{x}<br>Gross: $%{y:,.0f}")
            fig9.update_xaxes(title="Metascore")
            fig9.update_yaxes(title="Gross Revenue ($)")
            st.plotly_chart(apply_plotly_theme(fig9), use_container_width=True)
            
        # 10. Gross Revenue Distribution Histogram
        df_hist_gross = df.dropna(subset=['Gross_Clean'])
        fig10 = px.histogram(df_hist_gross, x='Gross_Clean', nbins=30, title="10. Distribution of Box Office Gross Revenues", color_discrete_sequence=[GOLD_COLOR])
        fig10.update_traces(hovertemplate="Revenue Range: $%{x}<br>Count: %{y}")
        fig10.update_xaxes(title="Gross Revenue Ranges ($)")
        fig10.update_yaxes(title="Number of Movies")
        st.plotly_chart(apply_plotly_theme(fig10, height=360), use_container_width=True)

    # STORY 3: Directors & Star Power
    with story3:
        st.subheader("Story 3: Directors & Star Power")
        c1, c2 = st.columns(2)
        
        with c1:
            # 11. Top Directors
            top_dirs = df['Director'].value_counts().head(10).reset_index()
            top_dirs.columns = ['Director', 'Count']
            fig11 = px.bar(top_dirs, x='Count', y='Director', orientation='h', title="11. Directors with Most Films in Dataset", color_discrete_sequence=[GOLD_COLOR])
            fig11.update_layout(yaxis=dict(autorange="reversed", title="Director Name"), xaxis=dict(title="Number of Movies"))
            fig11.update_traces(hovertemplate="<b>%{y}</b><br>Films: %{x}")
            st.plotly_chart(apply_plotly_theme(fig11), use_container_width=True)
            
            # 12. Lead Actors (Star 1)
            top_stars = df['Star1'].value_counts().head(10).reset_index()
            top_stars.columns = ['Star', 'Count']
            fig12 = px.bar(top_stars, x='Count', y='Star', orientation='h', title="12. Most Frequent Lead Actors (Star 1)", color_discrete_sequence=[GOLD_COLOR])
            fig12.update_layout(yaxis=dict(autorange="reversed", title="Actor Name"), xaxis=dict(title="Lead Roles Count"))
            fig12.update_traces(hovertemplate="<b>%{y}</b><br>Lead Roles: %{x}")
            st.plotly_chart(apply_plotly_theme(fig12), use_container_width=True)

        with c2:
            # 13. Highest Cumulative Grossing Directors
            dir_gross = df.groupby('Director')['Gross_Clean'].sum().nlargest(10).reset_index()
            fig13 = px.bar(dir_gross, x='Gross_Clean', y='Director', orientation='h', title="13. Top 10 Highest Grossing Directors ($)", color_discrete_sequence=[GOLD_COLOR])
            fig13.update_layout(yaxis=dict(autorange="reversed", title="Director"), xaxis=dict(title="Total Revenue ($)"))
            fig13.update_traces(hovertemplate="<b>%{y}</b><br>Total Gross: $%{x:,.0f}")
            st.plotly_chart(apply_plotly_theme(fig13), use_container_width=True)
            
            # 14. Top Rated Directors (Min 3 movies)
            dir_counts = df['Director'].value_counts()
            valid_dirs = dir_counts[dir_counts >= 3].index
            dir_ratings = df[df['Director'].isin(valid_dirs)].groupby('Director')['IMDB_Rating'].mean().nlargest(10).reset_index()
            
            fig14 = px.bar(dir_ratings, x='IMDB_Rating', y='Director', orientation='h', title="14. Highest Average Rated Directors (Min 3 Films)", color_discrete_sequence=[GOLD_COLOR])
            fig14.update_layout(yaxis=dict(autorange="reversed", title="Director"), xaxis=dict(range=[7.5, 9.0], title="Avg IMDb Rating"))
            fig14.update_traces(hovertemplate="<b>%{y}</b><br>Avg Rating: %{x:.2f}")
            st.plotly_chart(apply_plotly_theme(fig14), use_container_width=True)
            
        # 15. Runtime vs IMDb Rating Scatter
        df_runtime = df.dropna(subset=['Runtime_Min', 'IMDB_Rating'])
        fig15 = px.scatter(df_runtime, x='Runtime_Min', y='IMDB_Rating', hover_name='Series_Title', title="15. Runtime vs. IMDb Rating Relationship", color_discrete_sequence=[GOLD_COLOR])
        fig15.update_traces(marker=dict(size=7, opacity=0.7), hovertemplate="<b>%{hovertext}</b><br>Runtime: %{x} min<br>Rating: %{y}")
        fig15.update_xaxes(title="Runtime (Minutes)")
        fig15.update_yaxes(title="IMDb Rating")
        st.plotly_chart(apply_plotly_theme(fig15, height=360), use_container_width=True)

    # STORY 4: Genre Spectrum & Ratings
    with story4:
        st.subheader("Story 4: Genre Spectrum & Critical Reception")
        df_exploded = df.copy()
        df_exploded['Genre_List'] = df_exploded['Genre'].astype(str).str.split(', ')
        df_exploded = df_exploded.explode('Genre_List')
        
        c1, c2 = st.columns(2)
        with c1:
            # 16. Most Common Genres
            genre_counts = df_exploded['Genre_List'].value_counts().head(10).reset_index()
            genre_counts.columns = ['Genre', 'Count']
            
            fig16 = px.bar(genre_counts, x='Count', y='Genre', orientation='h', title="16. Most Popular Genres in Dataset", color_discrete_sequence=[GOLD_COLOR])
            fig16.update_layout(yaxis=dict(autorange="reversed", title="Genre"), xaxis=dict(title="Film Count"))
            fig16.update_traces(hovertemplate="<b>%{y}</b><br>Films: %{x}")
            st.plotly_chart(apply_plotly_theme(fig16), use_container_width=True)
            
            # 17. Highest Rated Genres
            genre_ratings = df_exploded.groupby('Genre_List')['IMDB_Rating'].mean().nlargest(10).reset_index()
            fig17 = px.bar(genre_ratings, x='IMDB_Rating', y='Genre_List', orientation='h', title="17. Highest Rated Genres (Avg IMDb Rating)", color_discrete_sequence=[GOLD_COLOR])
            fig17.update_layout(yaxis=dict(autorange="reversed", title="Genre"), xaxis=dict(range=[7.5, 8.5], title="Avg IMDb Rating"))
            fig17.update_traces(hovertemplate="<b>%{y}</b><br>Avg Rating: %{x:.2f}")
            st.plotly_chart(apply_plotly_theme(fig17), use_container_width=True)

        with c2:
            # 18. IMDb Rating Spread
            fig18 = px.histogram(df, x='IMDB_Rating', nbins=20, title="18. IMDb Rating Distribution", color_discrete_sequence=[GOLD_COLOR])
            fig18.update_traces(hovertemplate="Rating: %{x}<br>Count: %{y}")
            fig18.update_xaxes(title="IMDb Rating Scale")
            fig18.update_yaxes(title="Number of Movies")
            st.plotly_chart(apply_plotly_theme(fig18), use_container_width=True)
            
            # 19. Metascore vs IMDb Rating Alignment
            df_meta = df.dropna(subset=['Meta_score', 'IMDB_Rating'])
            fig19 = px.scatter(df_meta, x='Meta_score', y='IMDB_Rating', hover_name='Series_Title', title="19. Metascore vs. IMDb Rating Alignment", color_discrete_sequence=[GOLD_COLOR])
            fig19.update_traces(marker=dict(size=7, opacity=0.7), hovertemplate="<b>%{hovertext}</b><br>Metascore: %{x}<br>IMDb Rating: %{y}")
            fig19.update_xaxes(title="Metascore")
            fig19.update_yaxes(title="IMDb Rating")
            st.plotly_chart(apply_plotly_theme(fig19), use_container_width=True)
            
        # 20. Average Runtime per Genre
        genre_runtime = df_exploded.groupby('Genre_List')['Runtime_Min'].mean().sort_values(ascending=False).head(10).reset_index()
        fig20 = px.bar(genre_runtime, x='Runtime_Min', y='Genre_List', orientation='h', title="20. Average Movie Runtime per Genre", color_discrete_sequence=[GOLD_COLOR])
        fig20.update_layout(yaxis=dict(autorange="reversed", title="Genre"), xaxis=dict(title="Avg Runtime (Minutes)"))
        fig20.update_traces(hovertemplate="<b>%{y}</b><br>Avg Runtime: %{x:.1f} min")
        st.plotly_chart(apply_plotly_theme(fig20, height=360), use_container_width=True)

# -----------------------------------------------------------------------------
# 6. FOOTER WATERMARK
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    '''
    <div class="footer-watermark">
        APP AND DASHBOARD <strong>AFIQ HILMY</strong> &nbsp;|&nbsp; 
        <a href="https://linkedin.com/in/afiqhilmy" target="_blank">LINKEDIN.COM/IN/AFIQHILMY</a> &nbsp;|&nbsp;
        <a href="https://letterboxd.com/apiqqq" target="_blank">LETTERBOXD: APIQQQ</a>
    </div>
    ''',
    unsafe_allow_html=True
)
