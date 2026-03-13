import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UrbanAI — India Location Intelligence",
    page_icon="🏙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Nothing injected here — sidebar arrow is added inside main() below ──

# ─────────────────────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  /* Hide default streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 1.5rem 2rem 2rem; }

  /* App header */
  .app-header {
    display: flex; align-items: center; gap: 14px;
    padding: 1rem 0 1.4rem;
    border-bottom: 1px solid #272b38;
    margin-bottom: 1.5rem;
  }
  .app-logo-box {
    width: 42px; height: 42px; background: #e8622a; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-size: 20px;
  }
  .app-title {
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: 1.8rem; color: #e8622a; margin: 0; line-height: 1;
  }
  .app-sub { font-size: 0.82rem; color: #5e6880; margin-top: 2px; }

  /* Metric cards */
  .metric-card {
    background: #13151a; border: 1px solid #272b38; border-radius: 12px;
    padding: 1rem 1.2rem; text-align: center;
  }
  .metric-val {
    font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800;
    color: #e8622a; line-height: 1;
  }
  .metric-lbl { font-size: 0.72rem; color: #5e6880; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.06em; }

  /* Section labels */
  .sec-label {
    font-family: 'Syne', sans-serif; font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase; color: #5e6880;
    margin: 1.2rem 0 0.6rem;
  }

  /* Neighborhood cards */
  .nb-card {
    background: #13151a; border: 1px solid #272b38; border-radius: 14px;
    padding: 1.1rem 1.2rem; margin-bottom: 10px; cursor: pointer;
    transition: all 0.2s; position: relative; overflow: hidden;
  }
  .nb-card:hover { border-color: #e8622a44; }
  .nb-card-accent { position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #e8622a, #c94f8a); }
  .nb-rank { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800; color: #272b38; float: right; margin-top: -2px; }
  .nb-rank.top { color: #e8622a; }
  .nb-name { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; color: #dde3ee; }
  .nb-city { font-size: 0.74rem; color: #5e6880; margin-top: 2px; margin-bottom: 10px; }
  .score-row { display: flex; align-items: center; gap: 8px; }
  .score-bar-bg { flex: 1; height: 5px; background: #272b38; border-radius: 3px; overflow: hidden; }
  .score-bar-fill { height: 100%; background: linear-gradient(90deg, #c94f8a, #e8622a); border-radius: 3px; }
  .score-val { font-family: 'Syne', sans-serif; font-size: 0.82rem; font-weight: 700; color: #e8622a; min-width: 32px; }

  /* Tags */
  .tag { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 0.68rem; font-weight: 600; margin: 2px 2px 0 0; }
  .tag-orange { background: rgba(232,98,42,0.12); color: #e8622a; }
  .tag-pink   { background: rgba(201,79,138,0.12); color: #c94f8a; }
  .tag-amber  { background: rgba(245,166,35,0.12); color: #f5a623; }

  /* Rental cards */
  .rent-card {
    background: #13151a; border: 1px solid #272b38; border-radius: 12px;
    padding: 1rem; margin-bottom: 9px;
  }
  .rent-price { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800; color: #e8622a; }
  .rent-name  { font-family: 'Syne', sans-serif; font-size: 0.92rem; font-weight: 700; color: #dde3ee; }
  .rent-loc   { font-size: 0.74rem; color: #5e6880; }

  /* Sidebar hidden — not used in this layout */
  [data-testid="stSidebar"] { display: none !important; }
  [data-testid="collapsedControl"] { display: none !important; }

  /* Password modal */
  .pw-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.75); z-index: 10000;
    align-items: center; justify-content: center;
  }
  .pw-overlay.open { display: flex; }
  .pw-box {
    background: #13151a; border: 1px solid #272b38; border-radius: 16px;
    padding: 2rem 2rem 1.5rem; width: 340px;
    box-shadow: 0 24px 80px rgba(0,0,0,0.6);
  }
  .pw-box h3 { font-family:'Syne',sans-serif; color:#e8622a; margin:0 0 0.3rem; font-size:1.1rem; }
  .pw-box p  { color:#5e6880; font-size:0.8rem; margin:0 0 1.2rem; }
  .pw-box input {
    width:100%; padding:0.55rem 0.85rem; background:#1a1d25;
    border:1px solid #272b38; border-radius:8px; color:#dde3ee;
    font-size:0.9rem; box-sizing:border-box; outline:none; margin-bottom:0.75rem;
  }
  .pw-box input:focus { border-color:#e8622a; }
  .pw-box .pw-btn {
    width:100%; padding:0.6rem; background:#e8622a; color:#fff;
    border:none; border-radius:8px; font-family:'Syne',sans-serif;
    font-weight:700; font-size:0.88rem; cursor:pointer;
  }
  .pw-box .pw-btn:hover { background:#d4541f; }
  .pw-err { color:#e84040; font-size:0.76rem; margin-top:0.35rem; display:none; }

  /* Plotly charts background */
  .js-plotly-plot { border-radius: 12px; overflow: hidden; }

  /* Buttons */
  .stButton > button {
    background: #e8622a; color: white; border: none; border-radius: 8px;
    font-family: 'Syne', sans-serif; font-weight: 700; width: 100%;
    padding: 0.6rem 1rem; font-size: 0.9rem;
  }
  .stButton > button:hover { background: #d4541f; transform: translateY(-1px); }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #272b38; }
  .stTabs [data-baseweb="tab"] {
    background: transparent; color: #5e6880; border-radius: 6px;
    font-family: 'DM Sans', sans-serif; font-size: 0.84rem;
    padding: 6px 16px; border: 1px solid transparent;
  }
  .stTabs [aria-selected="true"] {
    background: #1a1d25 !important; color: #e8622a !important;
    border-color: #272b38 !important;
  }

  /* Selectbox */
  .stSelectbox > div > div { background: #1a1d25; border-color: #272b38; border-radius: 8px; color: #dde3ee; }

  /* Multiselect */
  .stMultiSelect > div > div { background: #1a1d25; border-color: #272b38; }

  /* Info/warning boxes */
  .stInfo { background: rgba(232,98,42,0.08); border-left-color: #e8622a; border-radius: 8px; }

  /* Dividers */
  hr { border-color: #272b38; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(cities_file, nb_file, rentals_file):
    """Load and clean all three CSVs."""

    # Cities — straightforward
    cities = pd.read_csv(cities_file)
    cities.columns = cities.columns.str.strip()
    num_city_cols = [c for c in cities.columns if c not in ('city','state')]
    cities[num_city_cols] = cities[num_city_cols].apply(pd.to_numeric, errors='coerce')

    # Neighborhoods — known_for has unquoted commas, so re-join overflow cols
    raw = []
    import csv, io
    content = nb_file.read().decode('utf-8') if hasattr(nb_file, 'read') else open(nb_file).read()
    reader = csv.reader(io.StringIO(content))
    headers = next(reader)
    n_fixed = len(headers)          # 17
    known_for_idx = headers.index('known_for')
    for row in reader:
        if len(row) > n_fixed:
            # merge extra fields back into known_for
            fixed = row[:known_for_idx]
            fixed.append(', '.join(row[known_for_idx:]))
            row = fixed
        raw.append(row)
    neighborhoods = pd.DataFrame(raw, columns=headers)
    neighborhoods.columns = neighborhoods.columns.str.strip()
    num_nb_cols = ['latitude','longitude','safety_score','transport_score','greenery_score',
                   'market_score','healthcare_score','schools_score','lifestyle_score',
                   'avg_rent_1bhk','avg_rent_2bhk','avg_rent_3bhk','cost_of_living_index','population_density']
    for c in num_nb_cols:
        if c in neighborhoods.columns:
            neighborhoods[c] = pd.to_numeric(neighborhoods[c], errors='coerce').fillna(0)

    # Rentals — has some bad lines
    content_r = rentals_file.read().decode('utf-8') if hasattr(rentals_file, 'read') else open(rentals_file).read()
    rentals = pd.read_csv(io.StringIO(content_r), on_bad_lines='skip')
    rentals.columns = rentals.columns.str.strip()
    for c in ['bedrooms','bathrooms','area_sqft','rent_per_month','floor','total_floors']:
        if c in rentals.columns:
            rentals[c] = pd.to_numeric(rentals[c], errors='coerce').fillna(0).astype(int)

    return cities, neighborhoods, rentals


@st.cache_data
def load_default_data():
    import csv, io, os
    base = os.path.dirname(__file__)
    cities = pd.read_csv(os.path.join(base, 'cities.csv'))
    cities.columns = cities.columns.str.strip()
    num_city_cols = [c for c in cities.columns if c not in ('city','state')]
    cities[num_city_cols] = cities[num_city_cols].apply(pd.to_numeric, errors='coerce')

    raw = []
    with open(os.path.join(base, 'neighborhoods.csv')) as f:
        reader = csv.reader(f)
        headers = next(reader)
        n_fixed = len(headers)
        known_for_idx = headers.index('known_for')
        for row in reader:
            if len(row) > n_fixed:
                fixed = row[:known_for_idx]
                fixed.append(', '.join(row[known_for_idx:]))
                row = fixed
            raw.append(row)
    neighborhoods = pd.DataFrame(raw, columns=headers)
    neighborhoods.columns = neighborhoods.columns.str.strip()
    num_nb_cols = ['latitude','longitude','safety_score','transport_score','greenery_score',
                   'market_score','healthcare_score','schools_score','lifestyle_score',
                   'avg_rent_1bhk','avg_rent_2bhk','avg_rent_3bhk','cost_of_living_index','population_density']
    for c in num_nb_cols:
        if c in neighborhoods.columns:
            neighborhoods[c] = pd.to_numeric(neighborhoods[c], errors='coerce').fillna(0)

    rentals = pd.read_csv(os.path.join(base, 'rentals.csv'), on_bad_lines='skip')
    rentals.columns = rentals.columns.str.strip()
    for c in ['bedrooms','bathrooms','area_sqft','rent_per_month','floor','total_floors']:
        if c in rentals.columns:
            rentals[c] = pd.to_numeric(rentals[c], errors='coerce').fillna(0).astype(int)

    return cities, neighborhoods, rentals


# ─────────────────────────────────────────────────────────────
# SCORING ENGINE
# ─────────────────────────────────────────────────────────────
def score_neighborhoods(df, prefs, weights, budget):
    df = df.copy()

    # Affordability score
    df['cost_score'] = df['cost_of_living_index'].apply(
        lambda x: max(10, 100 - x) if x > 0 else 50
    )
    # fallback: derive from rent if col is zero
    mask = df['cost_of_living_index'] == 0
    df.loc[mask, 'cost_score'] = df.loc[mask, 'avg_rent_2bhk'].apply(
        lambda r: max(10, round(100 - (r / budget) * 80)) if budget > 0 else 50
    )

    score_cols = {
        'cost':       ('cost_score',       weights['cost']    * (1.5 if 'cost'       in prefs else 0.7)),
        'safety':     ('safety_score',     weights['safety']  * (1.4 if 'safety'     in prefs else 0.7)),
        'transport':  ('transport_score',  weights['transit'] * (1.4 if 'transport'  in prefs else 0.7)),
        'green':      ('greenery_score',   weights['amen']    * (1.3 if 'green'      in prefs else 0.5)),
        'markets':    ('market_score',     5                  * (1.3 if 'markets'    in prefs else 0.6)),
        'healthcare': ('healthcare_score', 4                  * (1.3 if 'healthcare' in prefs else 0.6)),
        'schools':    ('schools_score',    4                  * (1.3 if 'schools'    in prefs else 0.5)),
        'lifestyle':  ('lifestyle_score',  4                  * (1.2 if 'lifestyle'  in prefs else 0.6)),
    }

    total, weight_sum = 0, 0
    for key, (col, w) in score_cols.items():
        vals = pd.to_numeric(df[col], errors='coerce').fillna(50)
        total += vals * w
        weight_sum += w

    df['overall_score'] = (total / weight_sum).round().astype(int)
    # Use the cheapest available BHK rent to check budget (so 1BHK listings count too)
    df['min_rent'] = df[['avg_rent_1bhk','avg_rent_2bhk','avg_rent_3bhk']].replace(0, float('nan')).min(axis=1).fillna(df['avg_rent_2bhk'])
    df['in_budget'] = df['min_rent'] <= budget
    return df.sort_values('overall_score', ascending=False).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='#13151a',
    plot_bgcolor='#13151a',
    font=dict(family='DM Sans', color='#8c95aa', size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    showlegend=False,
)

def bar_chart(df, x_col, y_col, title, color='#e8622a', orientation='h', text_col=None):
    if orientation == 'h':
        fig = px.bar(df, x=x_col, y=y_col, orientation='h',
                     color_discrete_sequence=[color], title=title)
        fig.update_traces(marker_color=color, textposition='inside',
                          text=df[x_col] if text_col is None else df[text_col])
    else:
        fig = px.bar(df, x=x_col, y=y_col,
                     color_discrete_sequence=[color], title=title)
    fig.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=13, color='#5e6880', family='Syne'))
    fig.update_xaxes(showgrid=False, color='#5e6880')
    fig.update_yaxes(showgrid=False, color='#5e6880')
    return fig


def radar_chart(nb_row):
    categories = ['Safety', 'Transit', 'Greenery', 'Markets', 'Healthcare', 'Schools', 'Lifestyle', 'Affordability']
    values = [
        float(nb_row.get('safety_score', 50)),
        float(nb_row.get('transport_score', 50)),
        float(nb_row.get('greenery_score', 50)),
        float(nb_row.get('market_score', 50)),
        float(nb_row.get('healthcare_score', 50)),
        float(nb_row.get('schools_score', 50)),
        float(nb_row.get('lifestyle_score', 50)),
        float(nb_row.get('cost_score', 50)),
    ]
    values_closed = values + [values[0]]
    categories_closed = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed, theta=categories_closed,
        fill='toself', fillcolor='rgba(232,98,42,0.15)',
        line=dict(color='#e8622a', width=2),
        marker=dict(color='#e8622a', size=6),
        name=nb_row.get('neighborhood', '')
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='#5e6880',
                           gridcolor='#272b38', tickfont=dict(size=9)),
            angularaxis=dict(color='#8c95aa', gridcolor='#272b38'),
            bgcolor='#13151a'
        ),
        **PLOTLY_LAYOUT,
        title=f"Score breakdown — {nb_row.get('neighborhood', '')}",
        title_font=dict(size=13, color='#5e6880', family='Syne'),
        height=350
    )
    return fig


def scatter_rent_score(df):
    fig = px.scatter(
        df, x='avg_rent_2bhk', y='overall_score',
        hover_name='neighborhood',
        hover_data={'avg_rent_2bhk': ':,.0f', 'overall_score': True, 'safety_score': True},
        color='overall_score',
        color_continuous_scale=['#272b38', '#e8622a', '#c94f8a'],
        size='overall_score', size_max=18,
        title='Rent vs Match Score'
    )
    fig.update_layout(**PLOTLY_LAYOUT,
                      title_font=dict(size=13, color='#5e6880', family='Syne'),
                      coloraxis_showscale=False)
    fig.update_xaxes(title='Avg 2BHK Rent (₹/mo)', showgrid=True, gridcolor='#1e2330', color='#5e6880')
    fig.update_yaxes(title='Match Score', showgrid=True, gridcolor='#1e2330', color='#5e6880')
    return fig


def heatmap_correlation(df):
    score_cols = ['safety_score','transport_score','greenery_score','market_score',
                  'healthcare_score','schools_score','lifestyle_score','avg_rent_2bhk']
    available = [c for c in score_cols if c in df.columns]
    corr = df[available].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale=[[0,'#13151a'], [0.5,'rgba(232,98,42,0.33)'], [1,'#e8622a']],
        text=corr.round(2).values, texttemplate='%{text}',
        textfont=dict(size=10, color='#dde3ee'),
        hovertemplate='%{x} × %{y}: %{z:.2f}<extra></extra>'
    ))
    fig.update_layout(**PLOTLY_LAYOUT,
                      title='Score Correlations', height=380,
                      title_font=dict(size=13, color='#5e6880', family='Syne'))
    return fig


def city_comparison_chart(cities_df, metric, city_list):
    subset = cities_df[cities_df['city'].isin(city_list)].copy()
    if metric not in subset.columns:
        return None
    subset = subset.sort_values(metric, ascending=False)
    colors = ['#e8622a' if i == 0 else '#c94f8a' if i == 1 else '#f5a623' if i == 2 else '#272b38'
              for i in range(len(subset))]
    fig = go.Figure(go.Bar(
        x=subset['city'], y=subset[metric],
        marker_color=colors,
        text=subset[metric].round(1), textposition='outside',
        textfont=dict(color='#8c95aa', size=11)
    ))
    fig.update_layout(**PLOTLY_LAYOUT,
                      title=metric.replace('_',' ').title(),
                      title_font=dict(size=13, color='#5e6880', family='Syne'),
                      height=300)
    fig.update_yaxes(showgrid=True, gridcolor='#1e2330', color='#5e6880')
    fig.update_xaxes(color='#5e6880')
    return fig


# ─────────────────────────────────────────────────────────────
# TAB 1: FILTERS
# ─────────────────────────────────────────────────────────────
def tab_filters(cities_df, nb_df, rentals_df):
    """City selector + all filters — renders inside Tab 0."""

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1d25,#13151a);border:1px solid #272b38;
                border-radius:16px;padding:2rem 2.5rem;margin-bottom:2rem">
      <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:#e8622a;margin-bottom:6px">
        Find your perfect neighborhood
      </div>
      <div style="color:#5e6880;font-size:0.9rem;max-width:600px">
        Choose your city, set your priorities, and we'll score every neighborhood for you.
      </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="sec-label">Select City</div>', unsafe_allow_html=True)
        city_options = sorted(nb_df['city'].dropna().unique().tolist())
        selected_city = st.selectbox('City', city_options,
                                     label_visibility='collapsed', key='city_sel')

        nb_in_city = len(nb_df[nb_df['city'] == selected_city])
        st.markdown(f'<div style="font-size:0.75rem;color:#5e6880;margin-top:-8px;margin-bottom:16px">'
                    f'{nb_in_city} neighborhoods available in {selected_city}</div>',
                    unsafe_allow_html=True)

        st.markdown('<div class="sec-label">What matters to you?</div>', unsafe_allow_html=True)
        pref_options = [
            ('💰 Low Cost', 'cost'), ('🛡 Safety', 'safety'),
            ('🌳 Greenery', 'green'), ('🚌 Transport', 'transport'),
            ('🛒 Markets', 'markets'), ('✨ Lifestyle', 'lifestyle'),
            ('🎓 Schools', 'schools'), ('🏥 Healthcare', 'healthcare'),
        ]
        selected_prefs = []
        pc1, pc2 = st.columns(2)
        for i, (label, key) in enumerate(pref_options):
            col = pc1 if i % 2 == 0 else pc2
            default = key in ('cost', 'safety', 'transport')
            if col.checkbox(label, value=default, key=f'pref_{key}'):
                selected_prefs.append(key)

        st.markdown('<div class="sec-label" style="margin-top:1.4rem">Max Rent Budget / Month</div>',
                    unsafe_allow_html=True)
        budget = st.slider('Budget', 5000, 200000, 40000, step=1000,
                           format='₹%d', label_visibility='collapsed', key='budget')
        st.markdown(
            f'<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;'
            f'color:#e8622a;margin-top:-4px">₹{budget:,} <span style="font-size:0.8rem;'
            f'font-weight:400;color:#5e6880">per month</span></div>',
            unsafe_allow_html=True)

    with right:
        st.markdown('<div class="sec-label">Fine-tune Importance</div>', unsafe_allow_html=True)
        w_cost    = st.slider('Affordability weight', 1, 10, 8, key='w_cost')
        w_safety  = st.slider('Safety weight',        1, 10, 7, key='w_safety')
        w_transit = st.slider('Transit weight',       1, 10, 6, key='w_transit')
        w_amen    = st.slider('Amenities weight',     1, 10, 5, key='w_amen')

        st.markdown('<br>', unsafe_allow_html=True)

        # ── Source Files (password-protected) ───────────────────
        st.markdown('<div class="sec-label">Admin</div>', unsafe_allow_html=True)
        if st.button("🗂 Source Files", use_container_width=True, key='src_btn'):
            st.session_state['show_src_panel'] = not st.session_state.get('show_src_panel', False)
            if not st.session_state.get('src_unlocked'):
                st.session_state.pop('src_pw_input', None)

        if st.session_state.get('show_src_panel') and not st.session_state.get('src_unlocked'):
            st.markdown('<div style="background:#1a1d25;border:1px solid #272b38;'
                        'border-radius:10px;padding:1rem;margin-top:0.5rem">',
                        unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.78rem;color:#dde3ee;font-weight:600;'
                        'margin-bottom:6px">🔒 Admin Password</div>', unsafe_allow_html=True)
            pw = st.text_input('pw', type='password', key='src_pw_input',
                               label_visibility='collapsed', placeholder='Enter password')
            if pw == '1234':
                st.session_state['src_unlocked'] = True
                st.rerun()
            elif pw:
                st.markdown('<div style="color:#e84040;font-size:0.75rem;margin-top:4px">'
                            'Incorrect password.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Full-width CSV editor (shown when unlocked) ────────────
    import os
    base_dir = os.path.dirname(__file__)

    if st.session_state.get('show_src_panel') and st.session_state.get('src_unlocked'):
        st.markdown('<hr style="border-color:#272b38;margin:1.5rem 0 1rem">', unsafe_allow_html=True)
        st.markdown(f'''
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
          <div>
            <div style="font-family:Syne,sans-serif;font-weight:700;color:#e8622a;font-size:1rem">
              🔓 Source File Editor
            </div>
            <div style="font-size:0.75rem;color:#5e6880;margin-top:2px">
              Edit data directly. Click Save after making changes.
            </div>
          </div>
        </div>
        ''', unsafe_allow_html=True)

        file_tab1, file_tab2, file_tab3 = st.tabs([
            f"🏙 cities.csv  ({len(cities_df)} rows)",
            f"🏘 neighborhoods.csv  ({len(nb_df)} rows)",
            f"🏠 rentals.csv  ({len(rentals_df)} rows)",
        ])

        def save_csv(df, filename):
            path = os.path.join(base_dir, filename)
            df.to_csv(path, index=False)
            st.cache_data.clear()

        with file_tab1:
            edited_cities = st.data_editor(
                cities_df, use_container_width=True, num_rows='dynamic',
                key='editor_cities', height=420
            )
            col_s, col_x = st.columns([1, 5])
            with col_s:
                if st.button('💾 Save cities.csv', key='save_cities', use_container_width=True):
                    save_csv(edited_cities, 'cities.csv')
                    st.success('✓ cities.csv saved!')
                    st.rerun()

        with file_tab2:
            edited_nb = st.data_editor(
                nb_df, use_container_width=True, num_rows='dynamic',
                key='editor_nb', height=420
            )
            col_s, col_x = st.columns([1, 5])
            with col_s:
                if st.button('💾 Save neighborhoods.csv', key='save_nb', use_container_width=True):
                    save_csv(edited_nb, 'neighborhoods.csv')
                    st.success('✓ neighborhoods.csv saved!')
                    st.rerun()

        with file_tab3:
            edited_rentals = st.data_editor(
                rentals_df, use_container_width=True, num_rows='dynamic',
                key='editor_rentals', height=420
            )
            col_s, col_x = st.columns([1, 5])
            with col_s:
                if st.button('💾 Save rentals.csv', key='save_rentals', use_container_width=True):
                    save_csv(edited_rentals, 'rentals.csv')
                    st.success('✓ rentals.csv saved!')
                    st.rerun()

        lock_col, _ = st.columns([1, 4])
        with lock_col:
            if st.button('🔒 Lock & Close', key='lock_btn', use_container_width=True):
                st.session_state['src_unlocked'] = False
                st.session_state['show_src_panel'] = False
                st.rerun()
        st.markdown('<hr style="border-color:#272b38;margin:1rem 0 1.5rem">', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        analyze = st.button('🔍  Find Best Neighborhoods', use_container_width=True,
                            key='analyze_btn', type='primary')

    weights = {'cost': w_cost, 'safety': w_safety, 'transit': w_transit, 'amen': w_amen}
    return selected_city, selected_prefs, weights, budget, analyze



# ─────────────────────────────────────────────────────────────
def tab_rankings(scored_df, budget):
    in_budget = scored_df[scored_df['in_budget']].shape[0]
    avg_score = int(scored_df['overall_score'].mean())
    avg_rent  = int(scored_df['avg_rent_2bhk'].mean())
    top_score = int(scored_df['overall_score'].max())

    m1, m2, m3, m4 = st.columns(4)
    for col, val, lbl in [(m1, len(scored_df), 'Areas Found'),
                           (m2, in_budget,      'In Budget'),
                           (m3, avg_score,      'Avg Score'),
                           (m4, top_score,      'Top Score')]:
        col.markdown(f'<div class="metric-card"><div class="metric-val">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)

    sort_col, filter_col = st.columns([1, 2])
    with sort_col:
        sort_by = st.selectbox('Sort by', ['Best Match','Cheapest','Safest','Best Transit','Most Green'])
    with filter_col:
        show_only_budget = st.checkbox('Show only in-budget neighborhoods', value=False)

    sort_map = {
        'Best Match':   ('overall_score', False),
        'Cheapest':     ('avg_rent_2bhk', True),
        'Safest':       ('safety_score',  False),
        'Best Transit': ('transport_score', False),
        'Most Green':   ('greenery_score', False),
    }
    s_col, s_asc = sort_map[sort_by]
    display_df = scored_df[scored_df['in_budget']] if show_only_budget else scored_df
    display_df = display_df.sort_values(s_col, ascending=s_asc).reset_index(drop=True)

    for i, (_, row) in enumerate(display_df.iterrows()):
        rank_class = 'top' if i < 3 else ''
        tags = []
        if row.get('safety_score', 0)    >= 80: tags.append('<span class="tag tag-orange">🛡 Safe</span>')
        if row.get('greenery_score', 0)  >= 70: tags.append('<span class="tag tag-pink">🌳 Green</span>')
        if row.get('transport_score', 0) >= 80: tags.append('<span class="tag tag-orange">🚇 Transit</span>')
        if row['in_budget']:                     tags.append('<span class="tag tag-amber">✓ Budget</span>')
        if row.get('lifestyle_score', 0) >= 80: tags.append('<span class="tag tag-pink">✨ Lifestyle</span>')

        # Build stat grid and tags outside the f-string to avoid rendering issues
        stat_items = [
            ('safety_score','Safety'), ('transport_score','Transit'), ('greenery_score','Green'),
            ('avg_rent_1bhk','1BHK'), ('avg_rent_2bhk','2BHK'), ('avg_rent_3bhk','3BHK')
        ]
        stat_grid = ''.join(
            f'<div style="background:#1a1d25;border-radius:6px;padding:5px;text-align:center">' +
            f'<div style="font-size:0.8rem;font-weight:600;color:#dde3ee">{int(row.get(c,0))}</div>' +
            f'<div style="font-size:0.62rem;color:#5e6880;margin-top:1px">{l}</div></div>'
            for c, l in stat_items
        )
        tags_html = ''.join(tags)
        city_known = row["city"] + (" · " + row["known_for"][:50] if row.get("known_for") else "")

        st.markdown(f"""
        <div class="nb-card">
          <div class="nb-card-accent"></div>
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div style="flex:1">
              <div class="nb-rank {rank_class}" style="float:right">#{i+1}</div>
              <div class="nb-name">{row['neighborhood']}</div>
              <div class="nb-city">{city_known}</div>
              <div class="score-row">
                <span style="font-size:0.72rem;color:#5e6880">Match</span>
                <div class="score-bar-bg"><div class="score-bar-fill" style="width:{row['overall_score']}%"></div></div>
                <span class="score-val">{row['overall_score']}</span>
              </div>
              <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:5px;margin:10px 0">
                {stat_grid}
              </div>
              {tags_html}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB: INSIGHTS
# ─────────────────────────────────────────────────────────────
def tab_insights(scored_df, cities_df, selected_city):
    city_row = cities_df[cities_df['city'] == selected_city]

    # Row 1: Score chart + Rent chart
    c1, c2 = st.columns(2)
    with c1:
        top8 = scored_df.head(8).copy()
        fig = go.Figure(go.Bar(
            x=top8['overall_score'], y=top8['neighborhood'],
            orientation='h', text=top8['overall_score'],
            textposition='inside', textfont=dict(color='#fff', size=11),
            marker=dict(color=top8['overall_score'],
                       colorscale=[[0,'#272b38'],[0.5,'#e8622a'],[1,'#c94f8a']],
                       showscale=False)
        ))
        fig.update_layout(**PLOTLY_LAYOUT, title='Top Areas by Score',
                          title_font=dict(size=13,color='#5e6880',family='Syne'),
                          height=320, yaxis=dict(autorange='reversed'))
        fig.update_xaxes(showgrid=True, gridcolor='#1e2330', color='#5e6880')
        fig.update_yaxes(color='#8c95aa')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        top8_rent = scored_df.head(8).sort_values('avg_rent_2bhk')
        fig2 = go.Figure(go.Bar(
            x=top8_rent['avg_rent_2bhk'], y=top8_rent['neighborhood'],
            orientation='h', text=top8_rent['avg_rent_2bhk'].apply(lambda x: f'₹{x:,.0f}'),
            textposition='inside', textfont=dict(color='#fff', size=10),
            marker_color='#c94f8a'
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, title='Avg 2BHK Rent / Month',
                           title_font=dict(size=13,color='#5e6880',family='Syne'),
                           height=320, yaxis=dict(autorange='reversed'))
        fig2.update_xaxes(showgrid=True, gridcolor='#1e2330', color='#5e6880',
                          tickformat='₹,.0f')
        fig2.update_yaxes(color='#8c95aa')
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2: Scatter + Radar
    c3, c4 = st.columns([1.2, 1])
    with c3:
        st.plotly_chart(scatter_rent_score(scored_df), use_container_width=True)
    with c4:
        if len(scored_df) > 0:
            top_nb = scored_df.iloc[0]
            st.plotly_chart(radar_chart(top_nb), use_container_width=True)

    # Row 3: Correlation heatmap
    st.plotly_chart(heatmap_correlation(scored_df), use_container_width=True)

    # Row 4: City-level CoL breakdown from cities.csv
    if not city_row.empty:
        st.markdown('<div class="sec-label" style="margin-top:1.5rem">Cost of Living — from cities.csv</div>', unsafe_allow_html=True)
        row = city_row.iloc[0]
        col_defs = [
            ('avg_monthly_expenses_single', 'Monthly (Single)',   lambda v: f'₹{v:,.0f}'),
            ('avg_monthly_expenses_family', 'Monthly (Family)',   lambda v: f'₹{v:,.0f}'),
            ('meal_cheap_restaurant',       'Cheap Meal',         lambda v: f'₹{v:.0f}'),
            ('meal_mid_restaurant',         'Mid Meal',           lambda v: f'₹{v:.0f}'),
            ('internet_cost',               'Internet / mo',      lambda v: f'₹{v:.0f}'),
            ('electricity_cost',            'Electricity / mo',   lambda v: f'₹{v:.0f}'),
            ('monthly_transport_pass',      'Transit Pass',       lambda v: f'₹{v:.0f}'),
            ('gym_monthly',                 'Gym / mo',           lambda v: f'₹{v:.0f}'),
            ('quality_of_life_score',       'Quality of Life',    lambda v: f'{v:.0f}/100'),
            ('pollution_index',             'Pollution Index',    lambda v: f'{v:.0f}/100'),
            ('traffic_index',               'Traffic Index',      lambda v: f'{v:.0f}/100'),
            ('healthcare_quality',          'Healthcare',         lambda v: f'{v:.0f}/100'),
            ('education_quality',           'Education',          lambda v: f'{v:.0f}/100'),
            ('teleport_score',              'Teleport Score',     lambda v: f'{v:.0f}/100'),
        ]
        valid = [(k,l,f) for k,l,f in col_defs if k in row.index and pd.notna(row[k]) and float(row[k]) != 0]
        if valid:
            cols_per_row = 4
            for chunk_start in range(0, len(valid), cols_per_row):
                chunk = valid[chunk_start:chunk_start+cols_per_row]
                mcols = st.columns(len(chunk))
                for col, (k, label, fmt) in zip(mcols, chunk):
                    col.markdown(f'<div class="metric-card"><div class="metric-val" style="font-size:1.2rem">{fmt(float(row[k]))}</div><div class="metric-lbl">{label}</div></div>', unsafe_allow_html=True)
                st.markdown('<br>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB: RENTALS
# ─────────────────────────────────────────────────────────────
def tab_rentals(rentals_df, selected_city, budget, scored_df):
    city_rentals = rentals_df[rentals_df['city'] == selected_city].copy()
    if city_rentals.empty:
        st.info(f"No rental listings found for {selected_city} in your rentals.csv")
        return

    # Filters row
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        areas = ['All'] + sorted(city_rentals['neighborhood'].dropna().unique().tolist())
        area_filter = st.selectbox('Neighborhood', areas)
    with f2:
        bhk_opts = ['All'] + sorted(city_rentals['bedrooms'].dropna().unique().astype(int).tolist())
        bhk_filter = st.selectbox('BHK', bhk_opts)
    with f3:
        furn_opts = ['All'] + sorted(city_rentals['furnishing'].dropna().unique().tolist())
        furn_filter = st.selectbox('Furnishing', furn_opts)
    with f4:
        only_budget = st.checkbox('Within my budget', value=False)

    # Apply filters
    df = city_rentals.copy()
    if area_filter != 'All':
        df = df[df['neighborhood'] == area_filter]
    if bhk_filter != 'All':
        df = df[df['bedrooms'] == int(bhk_filter)]
    if furn_filter != 'All':
        df = df[df['furnishing'] == furn_filter]
    if only_budget:
        df = df[df['rent_per_month'] <= budget]
    df = df.sort_values('rent_per_month')

    # Summary metrics
    if not df.empty:
        m1, m2, m3, m4 = st.columns(4)
        for col, val, lbl in [
            (m1, len(df),                              'Listings'),
            (m2, f"₹{int(df['rent_per_month'].min()):,}", 'Min Rent'),
            (m3, f"₹{int(df['rent_per_month'].mean()):,}", 'Avg Rent'),
            (m4, f"₹{int(df['rent_per_month'].max()):,}", 'Max Rent'),
        ]:
            col.markdown(f'<div class="metric-card"><div class="metric-val" style="font-size:1.1rem">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)

    # Rent distribution chart
    if len(df) > 2:
        fig = px.histogram(df, x='rent_per_month', nbins=20,
                           color_discrete_sequence=['#e8622a'],
                           title='Rent Distribution')
        fig.add_vline(x=budget, line_dash='dash', line_color='#c94f8a',
                      annotation_text='Your budget', annotation_font_color='#c94f8a')
        fig.update_layout(**PLOTLY_LAYOUT, height=220,
                          title_font=dict(size=13,color='#5e6880',family='Syne'))
        fig.update_xaxes(title='Rent (₹/mo)', color='#5e6880', tickformat='₹,.0f')
        fig.update_yaxes(title='Listings', color='#5e6880')
        st.plotly_chart(fig, use_container_width=True)

    # Cards
    if df.empty:
        st.info("No listings match your filters.")
        return

    num_cols = 3
    for row_start in range(0, len(df), num_cols):
        chunk = df.iloc[row_start:row_start+num_cols]
        cols = st.columns(num_cols)
        for col, (_, l) in zip(cols, chunk.iterrows()):
            over = l['rent_per_month'] > budget
            fur_color = '#e8622a' if l.get('furnishing') == 'Fully Furnished' else '#f5a623' if l.get('furnishing') == 'Semi-Furnished' else '#5e6880'
            raw_url  = str(l.get('listing_url', '')).strip()
            src_name = str(l.get('source', 'View Listing')).strip()
            if raw_url and raw_url.startswith('http'):
                listing_link_html = (
                    f'<a href="{raw_url}" target="_blank" rel="noopener noreferrer" '
                    f'style="display:block;margin-top:8px;padding:7px;background:#c94f8a;'
                    f'color:#fff;text-align:center;border-radius:7px;text-decoration:none;'
                    f'font-size:0.78rem;font-weight:700">🔗 View on {src_name}</a>'
                )
            else:
                listing_link_html = ""
            amenities = str(l.get('amenities','')).replace('|',',').split(',')
            amenities = [a.strip() for a in amenities if a.strip()][:4]
            typeRaw = str(l.get('property_type','')).lower()
            badge_color = '#c94f8a' if 'house' in typeRaw else '#f5a623' if 'flat' in typeRaw else '#e8622a'

            with col:
                st.markdown(f"""
                <div class="rent-card" style="{'opacity:0.6' if over else ''}">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <span style="background:{badge_color}22;color:{badge_color};padding:2px 8px;border-radius:20px;font-size:0.67rem;font-weight:700">{l.get('property_type','Property').upper()}</span>
                    {'<span style="font-size:0.68rem;color:#e84040">Over budget</span>' if over else ''}
                  </div>
                  <div class="rent-name" style="margin-top:6px">{l.get('property_name','Listing')}</div>
                  <div class="rent-loc">📍 {l.get('neighborhood','')}, {l.get('city','')}</div>
                  <div class="rent-price" style="margin:6px 0">₹{l['rent_per_month']:,}<span style="font-size:0.72rem;font-weight:400;color:#5e6880">/month</span></div>
                  <div style="display:flex;flex-wrap:wrap;gap:5px;margin:6px 0">
                    {'<span style="font-size:0.72rem;background:#1a1d25;padding:2px 7px;border-radius:5px;color:#8c95aa">🛏 '+str(l['bedrooms'])+' Bed</span>' if l.get('bedrooms') else ''}
                    {'<span style="font-size:0.72rem;background:#1a1d25;padding:2px 7px;border-radius:5px;color:#8c95aa">🚿 '+str(l['bathrooms'])+' Bath</span>' if l.get('bathrooms') else ''}
                    {'<span style="font-size:0.72rem;background:#1a1d25;padding:2px 7px;border-radius:5px;color:#8c95aa">📐 '+str(l['area_sqft'])+'sqft</span>' if l.get('area_sqft') else ''}
                    {'<span style="font-size:0.72rem;background:#1a1d25;padding:2px 7px;border-radius:5px;color:#8c95aa">🚗 Parking</span>' if l.get('parking')=='Yes' else ''}
                  </div>
                  {'<div style="font-size:0.7rem;color:'+fur_color+';margin-bottom:5px">'+str(l.get('furnishing',''))+'</div>' if l.get('furnishing') else ''}
                  {'<div style="font-size:0.7rem;color:#5e6880">'+' · '.join(amenities)+'</div>' if amenities else ''}
                  {'<div style="font-size:0.73rem;color:#5e6880;margin-top:6px;padding-top:6px;border-top:1px solid #272b38;line-height:1.5">'+str(l.get('description',''))[:100]+'...</div>' if l.get('description') else ''}
                  {listing_link_html}
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TAB: CITY COMPARE
# ─────────────────────────────────────────────────────────────
def tab_city_compare(cities_df, nb_df):
    st.markdown('<div style="font-size:0.82rem;color:#5e6880;margin-bottom:1rem">Compare cities side-by-side using data from your cities.csv</div>', unsafe_allow_html=True)

    all_cities = sorted(cities_df['city'].dropna().unique().tolist())
    selected = st.multiselect('Select cities to compare', all_cities,
                               default=all_cities[:5] if len(all_cities) >= 5 else all_cities)
    if not selected:
        st.info("Select at least 2 cities to compare.")
        return

    # Numeric columns available
    numeric_cols = [c for c in cities_df.columns
                    if c not in ('city','state') and pd.api.types.is_numeric_dtype(cities_df[c])]

    metric_groups = {
        '💰 Cost':        ['cost_of_living_index','avg_monthly_expenses_single','avg_monthly_expenses_family'],
        '🌱 Lifestyle':   ['quality_of_life_score','pollution_index','traffic_index','climate_score'],
        '🏥 Services':    ['healthcare_quality','education_quality','teleport_score'],
        '🍽 Daily Life':  ['meal_cheap_restaurant','meal_mid_restaurant','internet_cost','monthly_transport_pass'],
    }

    for group_name, cols in metric_groups.items():
        available = [c for c in cols if c in numeric_cols]
        if not available:
            continue
        st.markdown(f'<div class="sec-label" style="margin-top:1.2rem">{group_name}</div>', unsafe_allow_html=True)
        chart_cols = st.columns(min(len(available), 4))
        for col, metric in zip(chart_cols, available):
            fig = city_comparison_chart(cities_df, metric, selected)
            if fig:
                with col:
                    st.plotly_chart(fig, use_container_width=True)

    # Neighborhood count per city
    st.markdown('<div class="sec-label" style="margin-top:1.2rem">📊 Neighborhoods in Dataset</div>', unsafe_allow_html=True)
    nb_counts = nb_df[nb_df['city'].isin(selected)].groupby('city').size().reset_index(name='count')
    nb_counts = nb_counts.sort_values('count', ascending=False)
    fig_nb = go.Figure(go.Bar(
        x=nb_counts['city'], y=nb_counts['count'],
        marker_color='#e8622a', text=nb_counts['count'], textposition='outside',
        textfont=dict(color='#8c95aa')
    ))
    fig_nb.update_layout(**PLOTLY_LAYOUT, title='Neighborhood Coverage',
                         title_font=dict(size=13,color='#5e6880',family='Syne'),
                         height=280)
    fig_nb.update_yaxes(showgrid=True, gridcolor='#1e2330', color='#5e6880')
    fig_nb.update_xaxes(color='#5e6880')
    st.plotly_chart(fig_nb, use_container_width=True)

    # Full data table
    with st.expander("📋 Full City Data Table"):
        subset = cities_df[cities_df['city'].isin(selected)].set_index('city')
        st.dataframe(subset, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB: RAW DATA
# ─────────────────────────────────────────────────────────────
def tab_raw_data(cities_df, nb_df, rentals_df, selected_city):
    t1, t2, t3 = st.tabs(["🏙 Cities", "🏘 Neighborhoods", "🏠 Rentals"])
    with t1:
        st.markdown(f'<div style="font-size:0.78rem;color:#5e6880;margin-bottom:8px">{len(cities_df)} cities · {len(cities_df.columns)} columns</div>', unsafe_allow_html=True)
        st.dataframe(cities_df, use_container_width=True, height=400)
        st.download_button('⬇ Download cities.csv', cities_df.to_csv(index=False), 'cities.csv', 'text/csv')
    with t2:
        city_nb = nb_df[nb_df['city'] == selected_city]
        st.markdown(f'<div style="font-size:0.78rem;color:#5e6880;margin-bottom:8px">{len(city_nb)} neighborhoods in {selected_city} · {len(nb_df)} total</div>', unsafe_allow_html=True)
        st.dataframe(city_nb, use_container_width=True, height=400)
        st.download_button('⬇ Download neighborhoods.csv', nb_df.to_csv(index=False), 'neighborhoods.csv', 'text/csv')
    with t3:
        city_rent = rentals_df[rentals_df['city'] == selected_city]
        st.markdown(f'<div style="font-size:0.78rem;color:#5e6880;margin-bottom:8px">{len(city_rent)} listings in {selected_city} · {len(rentals_df)} total</div>', unsafe_allow_html=True)
        st.dataframe(city_rent, use_container_width=True, height=400)
        st.download_button('⬇ Download rentals.csv', rentals_df.to_csv(index=False), 'rentals.csv', 'text/csv')


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    # Load data
    if 'custom_data' in st.session_state:
        c_f, nb_f, re_f = st.session_state['custom_data']
        cities_df, nb_df, rentals_df = load_data(c_f, nb_f, re_f)
    else:
        cities_df, nb_df, rentals_df = load_default_data()

    # ── Header ─────────────────────────────────────────────────
    nb_count    = len(nb_df)
    rent_count  = len(rentals_df)
    city_count  = len(cities_df)
    st.markdown(f"""
    <div class="app-header">
      <div class="app-logo-box">🏙</div>
      <div>
        <div class="app-title">UrbanAI</div>
        <div class="app-sub">India Location Intelligence</div>
      </div>
      <div style="margin-left:auto;display:flex;gap:20px;align-items:center">
        <div style="text-align:center">
          <div style="font-family:Syne,sans-serif;font-weight:800;color:#e8622a;font-size:1.2rem">{nb_count}</div>
          <div style="font-size:0.67rem;color:#5e6880;text-transform:uppercase;letter-spacing:0.08em">Neighborhoods</div>
        </div>
        <div style="text-align:center">
          <div style="font-family:Syne,sans-serif;font-weight:800;color:#c94f8a;font-size:1.2rem">{rent_count}</div>
          <div style="font-size:0.67rem;color:#5e6880;text-transform:uppercase;letter-spacing:0.08em">Listings</div>
        </div>
        <div style="text-align:center">
          <div style="font-family:Syne,sans-serif;font-weight:800;color:#f5a623;font-size:1.2rem">{city_count}</div>
          <div style="font-size:0.67rem;color:#5e6880;text-transform:uppercase;letter-spacing:0.08em">Cities</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Decide which tab to show ────────────────────────────────
    # active_tab: 0=Filters, 1=Rankings, 2=Insights, 3=Rentals, 4=City Compare, 5=Map
    if 'active_tab' not in st.session_state:
        st.session_state['active_tab'] = 0

    TAB_LABELS = [
        "⚙️ Filters & City",
        "🏘 Rankings",
        "📊 Insights",
        "🏠 Rentals",
        "🏙 City Compare",
    ]

    tab0, tab1, tab2, tab3, tab4 = st.tabs(TAB_LABELS)

    # ── Tab 0: Filters ─────────────────────────────────────────
    with tab0:
        selected_city, prefs, weights, budget, do_analyze = tab_filters(
            cities_df, nb_df, rentals_df)

        # Run scoring whenever city changes or user clicks analyze
        if do_analyze or st.session_state.get('last_city') != selected_city:
            city_nb = nb_df[nb_df['city'] == selected_city]
            if not city_nb.empty:
                scored = score_neighborhoods(city_nb, prefs, weights, budget)
                st.session_state['scored_df']   = scored
                st.session_state['last_city']   = selected_city
                st.session_state['last_budget'] = budget

        if do_analyze and st.session_state.get('scored_df') is not None:
            # Auto-click the Rankings tab via JS in parent frame
            import streamlit.components.v1 as components
            components.html("""
            <script>
            (function(){
                function clickRankingsTab() {
                    var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
                    if (tabs && tabs.length > 1) { tabs[1].click(); return true; }
                    return false;
                }
                if (!clickRankingsTab()) {
                    var tries = 0;
                    var t = setInterval(function(){
                        if (clickRankingsTab() || ++tries > 10) clearInterval(t);
                    }, 150);
                }
            })();
            </script>
            """, height=0)

    # Pull scored data + budget from session (available across all tabs)
    scored_df = st.session_state.get('scored_df', pd.DataFrame())
    budget    = st.session_state.get('last_budget', 40000)
    selected_city = st.session_state.get('last_city',
                    sorted(nb_df['city'].dropna().unique().tolist())[0])

    # ── Tabs 1-5: Results ──────────────────────────────────────
    with tab1:
        if scored_df.empty:
            st.markdown("""
            <div style="text-align:center;padding:4rem 2rem;color:#5e6880">
              <div style="font-size:3rem;margin-bottom:1rem">🏘</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.1rem;color:#dde3ee;margin-bottom:8px">
                No results yet
              </div>
              <div style="font-size:0.85rem">
                Go to <b style="color:#e8622a">⚙️ Filters & City</b> tab, choose your city and preferences,
                then click <b style="color:#e8622a">Find Best Neighborhoods</b>.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            tab_rankings(scored_df, budget)

    with tab2:
        if scored_df.empty:
            st.info("Run a search from the **⚙️ Filters & City** tab first.")
        else:
            tab_insights(scored_df, cities_df, selected_city)

    with tab3:
        if scored_df.empty:
            st.info("Run a search from the **⚙️ Filters & City** tab first.")
        else:
            tab_rentals(rentals_df, selected_city, budget, scored_df)

    with tab4:
        tab_city_compare(cities_df, nb_df)

    # Raw data expander at bottom
    with st.expander("📋 Raw Data Explorer"):
        tab_raw_data(cities_df, nb_df, rentals_df, selected_city)


if __name__ == '__main__':
    main()