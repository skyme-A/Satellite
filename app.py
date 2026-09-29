import streamlit as st
import requests
from PIL import Image
import io
from datetime import datetime, timezone

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Gemini // Deep Space Downlink",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. EXACT GEMINI DARK THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Inter:wght@400;500;600&family=Roboto+Mono:wght@400;500&display=swap');

    /* Global Typography Reset */
    * {
        font-family: 'Google Sans', 'Inter', -apple-system, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Completely hide Streamlit default chrome & buttons */
    header[data-testid="stHeader"], footer, #MainMenu, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* Authentic Gemini Canvas: #131314 */
    .stApp {
        background-color: #131314 !important;
        color: #E3E3E3 !important;
    }

    .block-container {
        max-width: 920px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto;
    }

    /* Top Bar */
    .gemini-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.2rem;
        margin-bottom: 1.6rem;
        border-bottom: 1px solid #282A2C;
    }

    .gemini-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.2rem;
        font-weight: 500;
        color: #E3E3E3;
    }

    .sparkle-icon {
        font-size: 1.35rem;
        background: linear-gradient(135deg, #7Cacf8 0%, #a8c7fa 50%, #d3e3fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .status-text {
        font-family: 'Roboto Mono', monospace !important;
        font-size: 0.74rem;
        color: #8E918F;
        letter-spacing: 0.05em;
    }

    /* Gemini Heading with Gradient */
    .gemini-title {
        font-size: 1.95rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #A8C7FA 0%, #E3E3E3 60%, #C4C7C5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.35rem;
        line-height: 1.3;
    }

    .gemini-desc {
        font-size: 0.92rem;
        color: #C4C7C5;
        line-height: 1.6;
        margin-bottom: 1.4rem;
        font-weight: 400;
    }

    /* Gemini Pill Buttons */
    div.stButton > button {
        background-color: #1E1F20 !important;
        color: #C4C7C5 !important;
        border: 1px solid #37393B !important;
        border-radius: 20px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 6px 16px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    div.stButton > button:hover {
        background-color: #282A2C !important;
        color: #A8C7FA !important;
        border-color: #7Cacf8 !important;
    }

    /* Download Pill */
    div.stDownloadButton > button {
        background-color: #1E1F20 !important;
        color: #A8C7FA !important;
        border: 1px solid rgba(124, 172, 248, 0.3) !important;
        border-radius: 20px !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        padding: 6px 18px !important;
        transition: all 0.2s ease !important;
    }

    div.stDownloadButton > button:hover {
        background-color: #282A2C !important;
        border-color: #A8C7FA !important;
        color: #D3E3FD !important;
    }

    /* Clean Image Viewport Frame */
    .image-card-wrapper {
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid #282A2C;
        background-color: #1E1F20;
        padding: 10px;
        margin: 10px 0 20px 0;
    }

    /* Gemini Spec Bar */
    .gemini-data-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-top: 1.6rem;
        padding: 1.1rem 1.4rem;
        background-color: #1E1F20;
        border: 1px solid #282A2C;
        border-radius: 16px;
    }

    .metric-col {
        display: flex;
        flex-direction: column;
    }

    .metric-lbl {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #8E918F;
        margin-bottom: 4px;
        font-weight: 500;
    }

    .metric-val {
        font-size: 0.88rem;
        font-weight: 500;
        color: #E3E3E3;
    }

    @media (max-width: 768px) {
        .gemini-data-strip {
            grid-template-columns: repeat(2, 1fr);
            row-gap: 14px;
        }
        .gemini-title {
            font-size: 1.55rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ROBUST ASSET FETCHING ---
@st.cache_data(show_spinner=False)
def load_deep_space_image(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200:
            return Image.open(io.BytesIO(r.content))
    except Exception:
        pass
    return None

def apply_optical_crop(image: Image.Image, zoom_factor: int):
    if zoom_factor <= 1:
        return image
    width, height = image.size
    crop_w = width // zoom_factor
    crop_h = height // zoom_factor
    left = (width - crop_w) // 2
    top = (height - crop_h) // 2
    return image.crop((left, top, left + crop_w, top + crop_h))

# --- 4. CATALOG REGISTRY ---
CATALOG = {
    "Deep Cosmos": {
        "title": "M83 · The Southern Pinwheel Galaxy",
        "desc": "Grand-design spiral galaxy located 15 million light-years away in Hydra. Optical composite capturing young star clusters and interstellar dust lanes.",
        "instrument": "Hubble WFC3 Optical",
        "authority": "NASA / STScI / ESA",
        "distance": "15,030,000 Light-Years",
        "url": "https://cdn.eso.org/images/screen/eso1403a.jpg"
    },
    "The Sun (Photosphere)": {
        "title": "Solar Photosphere & Active Sunspot Clusters",
        "desc": "Visible continuum light scan from the Solar Dynamics Observatory isolating turbulent surface granulation and localized magnetic field lines.",
        "instrument": "SDO Helioseismic (HMI)",
        "authority": "NASA Goddard Space Flight Center",
        "distance": "149,600,000 Kilometers",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIC.jpg"
    },
    "The Sun (EUV Corona)": {
        "title": "Superheated Solar Corona (17.1 nm)",
        "desc": "Extreme ultraviolet imaging tracing magnetically confined iron plasma loops at 1,000,000 Kelvin in the upper transition envelope.",
        "instrument": "AIA 171 Å Extreme UV",
        "authority": "NASA Goddard Space Flight Center",
        "distance": "149,600,000 Kilometers",
        "url": "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg"
    },
    "Mars (Jezero Delta)": {
        "title": "Jezero Crater · Ancient River Alluvial Fan",
        "desc": "High-resolution orbital scan from MRO resolving preserved clay sediment layers where ancient rivers emptied into Lake Jezero billions of years ago.",
        "instrument": "HiRISE High-Res Camera",
        "authority": "NASA / JPL-Caltech",
        "distance": "225,400,000 Kilometers",
        "url": "https://cdn.eso.org/images/screen/eso0926a.jpg"
    },
    "Jupiter (Cloud Belts)": {
        "title": "Jovian Great Red Spot & Storm Belts",
        "desc": "Atmospheric sounding from the Juno spacecraft during close perijove transit, resolving ammonia-ice clouds and the ancient anticyclonic vortex.",
        "instrument": "JunoCam Optical Payload",
        "authority": "NASA / SwRI / MSSS",
        "distance": "778,500,000 Kilometers",
        "url": "https://cdn.eso.org/images/screen/eso1623a.jpg"
    }
}

# --- 5. TOP GEMINI MASTHEAD ---
st.markdown(f"""
    <div class="gemini-header">
        <div class="gemini-logo">
            <span class="sparkle-icon">✦</span>
            Aether Downlink
        </div>
        <div class="status-text">
            UTC {datetime.now(timezone.utc).strftime('%H:%M:%S')} &nbsp;•&nbsp; DSN CARRIER LOCKED
        </div>
    </div>
""", unsafe_allow_html=True)

# State initialization
if "selected_target" not in st.session_state:
    st.session_state.selected_target = "Deep Cosmos"

if "zoom" not in st.session_state:
    st.session_state.zoom = 1

# --- 6. GEMINI INTERACTIVE PILL CHIP BAR (NO DROPDOWNS) ---
chip_cols = st.columns(len(CATALOG))
for idx, key in enumerate(CATALOG.keys()):
    with chip_cols[idx]:
        is_selected = (st.session_state.selected_target == key)
        # Subtle visual indicator for active chip
        btn_label = f"✦ {key}" if is_selected else key
        if st.button(btn_label, key=f"chip_{key}", use_container_width=True):
            st.session_state.selected_target = key
            st.session_state.zoom = 1
            st.rerun()

current = CATALOG[st.session_state.selected_target]

# Title & Description
st.markdown(f'<div class="gemini-title">{current["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="gemini-desc">{current["desc"]}</div>', unsafe_allow_html=True)

# Controls Row (Soft Zoom Pills & Export Frame)
c_zoom, c_export = st.columns([6, 4])
with c_zoom:
    z1, z2, z3 = st.columns(3)
    with z1:
        if st.button("1× Wide", use_container_width=True):
            st.session_state.zoom = 1
            st.rerun()
    with z2:
        if st.button("2× Crop", use_container_width=True):
            st.session_state.zoom = 2
            st.rerun()
    with z3:
        if st.button("3× Core", use_container_width=True):
            st.session_state.zoom = 3
            st.rerun()

with c_export:
    raw_img = load_deep_space_image(current["url"])
    if raw_img:
        buf = io.BytesIO()
        raw_img.save(buf, format="PNG")
        st.download_button(
            label="↓ Export Raw Frame",
            data=buf.getvalue(),
            file_name=f"AETHER_{current['instrument'].split()[0]}_{datetime.now(timezone.utc).strftime('%Y%m%d')}.png",
            mime="image/png",
            use_container_width=True
        )

# --- 7. IMAGE VIEWPORT ---
if raw_img:
    rendered_img = apply_optical_crop(raw_img, st.session_state.zoom)
    st.image(rendered_img, use_container_width=True)
else:
    st.markdown('<div style="color: #8E918F; padding: 2rem 0; font-family: monospace;">Telemetric payload unavailable. Re-establishing link...</div>', unsafe_allow_html=True)

# --- 8. GEMINI DATA STRIP ---
st.markdown(f"""
    <div class="gemini-data-strip">
        <div class="metric-col">
            <span class="metric-lbl">Payload Instrument</span>
            <span class="metric-val">{current["instrument"]}</span>
        </div>
        <div class="metric-col">
            <span class="metric-lbl">Distance to Subject</span>
            <span class="metric-val">{current["distance"]}</span>
        </div>
        <div class="metric-col">
            <span class="metric-lbl">Operating Authority</span>
            <span class="metric-val">{current["authority"]}</span>
        </div>
        <div class="metric-col">
            <span class="metric-lbl">Link Telemetry</span>
            <span class="metric-val" style="color: #A8C7FA;">Synchronized</span>
        </div>
    </div>
""", unsafe_allow_html=True)