import streamlit as st
import swisseph as swe
from datetime import datetime, date, time as dtime
import requests
from life_financial_module import generate_life_financial_steps

# ==================== Swiss Ephemeris Setup ====================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)

# ==================== Constants ====================
PLANETS = {
    "সূর্য": swe.SUN,
    "চন্দ্র": swe.MOON,
    "মঙ্গল": swe.MARS,
    "বুধ": swe.MERCURY,
    "বৃহস্পতি": swe.JUPITER,
    "শুক্র": swe.VENUS,
    "শনি": swe.SATURN,
    "রাহু": swe.TRUE_NODE,
    "কেতু": swe.TRUE_NODE,
}

RASHIS_BN = [
    "মেষ", "বৃষ", "মিথুন", "কর্কট", "সিংহ", "কন্যা",
    "তুলা", "বৃশ্চিক", "ধনু", "মকর", "কুম্ভ", "মীন"
]

RASHIS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    ("অশ্বিনী", "Ashwini", "কেতু"),
    ("ভরণী", "Bharani", "শুক্র"),
    ("কৃত্তিকা", "Krittika", "সূর্য"),
    ("রোহিণী", "Rohini", "চন্দ্র"),
    ("মৃগশিরা", "Mrigashira", "মঙ্গল"),
    ("আর্দ্রা", "Ardra", "রাহু"),
    ("পুনর্বসু", "Punarvasu", "বৃহস্পতি"),
    ("পুষ্যা", "Pushya", "শনি"),
    ("অশ্লেষা", "Ashlesha", "বুধ"),
    ("মঘা", "Magha", "কেতু"),
    ("পূর্বফাল্গুনী", "Purva Phalguni", "শুক্র"),
    ("উত্তরফাল্গুনী", "Uttara Phalguni", "সূর্য"),
    ("হস্তা", "Hasta", "চন্দ্র"),
    ("চিত্রা", "Chitra", "মঙ্গল"),
    ("স্বাতী", "Swati", "রাহু"),
    ("বিশাখা", "Vishakha", "বৃহস্পতি"),
    ("অনুরাধা", "Anuradha", "শনি"),
    ("জ্যেষ্ঠা", "Jyeshtha", "বুধ"),
    ("মূলা", "Mula", "কেতু"),
    ("পূর্বাষাঢা", "Purva Ashadha", "শুক্র"),
    ("উত্তরাষাঢা", "Uttara Ashadha", "সূর্য"),
    ("শ্রবণা", "Shravana", "চন্দ্র"),
    ("ধনিষ্ঠা", "Dhanishta", "মঙ্গল"),
    ("শতভিষা", "Shatabhisha", "রাহু"),
    ("পূর্বভাদ্রপদ", "Purva Bhadrapada", "বৃহস্পতি"),
    ("উত্তরভাদ্রপদ", "Uttara Bhadrapada", "শনি"),
    ("রেবতী", "Revati", "বুধ"),
]

NAKSHATRA_CHARACTER = {
    "অশ্বিনী": "দ্রুত কাজ করা, সাহসী, চিকিৎসা ও যাতায়াতে আগ্রহী। নেতৃত্বের গুণ আছে।",
    "ভরণী": "সৃজনশীল, কঠোর পরিশ্রমী, ন্যায়পরায়ণ। শিল্প ও সৌন্দর্য প্রিয়।",
    "কৃত্তিকা": "তেজস্বী, নেতৃত্বের গুণসম্পন্ন, পরিষ্কার-পরিচ্ছন্নতা প্রিয়। তীক্ষ্ণ বুদ্ধি।",
    "রোহিণী": "শান্ত, সৃজনশীল, স্থির মনের, সৌন্দর্য প্রিয়। লক্ষ্মীর আশীর্বাদ।",
    "মৃগশিরা": "অনুসন্ধিৎসু, কোমল স্বভাবের, শিল্প ও সঙ্গীতে আগ্রহী। পরিভ্রমণ প্রিয়।",
    "আর্দ্রা": "গভীর চিন্তাশীল, আবেগপ্রবণ, পরিবর্তনপ্রিয়। তীব্র অনুভূতিসম্পন্ন।",
    "পুনর্বসু": "দয়ালু, ধৈর্যশীল, পুনরুত্থানের শক্তি রাখে। শিক্ষা ও পরামর্শে দক্ষ।",
    "পুষ্যা": "পুষ্টিকর, ধার্মিক, লালন-পালনে পারদর্শী। রাজযোগের সম্ভাবনা।",
    "অশ্লেষা": "তীক্ষ্ণ বুদ্ধিসম্পন্ন, গোপনীয়তা প্রিয়, কৌশলী। গবেষণায় দক্ষ।",
    "মঘা": "রাজসিক, সম্মানপ্রিয়, পূর্বপুরুষের প্রতি শ্রদ্ধাশীল। কর্তৃত্বপূর্ণ।",
    "পূর্বফাল্গুনী": "আনন্দপ্রিয়, সামাজিক, শিল্পকলায় দক্ষ। ভোগ ও বিলাসিতা প্রিয়।",
    "উত্তরফাল্গুনী": "বিশ্বস্ত, দায়িত্বশীল, স্থিতিশীল ও সহায়ক স্বভাবের। পরিবারকেন্দ্রিক।",
    "হস্তা": "দক্ষ হাতের কাজ, ব্যবসায়ী মানসিকতা, নিখুঁত কাজ করে। কারিগরি দক্ষতা।",
    "চিত্রা": "সৌন্দর্যবোধ সম্পন্ন, শিল্পী স্বভাবের, আকর্ষণীয় ব্যক্তিত্ব। ডিজাইন ও ফ্যাশন।",
    "স্বাতী": "স্বাধীনচেতা, নমনীয়, বায়ুমণ্ডলীয় ও পরিবর্তনশীল। ব্যবসায় সফল।",
    "বিশাখা": "লক্ষ্যভেদী, দ্বৈত স্বভাবের, সাফল্যের জন্য কঠোর পরিশ্রমী। উচ্চাকাঙ্ক্ষী।",
    "অনুরাধা": "বন্ধুত্বপূর্ণ, ভক্তিমূলক, গভীর সম্পর্ক গড়ে তোলে। সংগঠন ক্ষমতা।",
    "জ্যেষ্ঠা": "নেতৃত্বদানের ক্ষমতা, রক্ষাকারী স্বভাব, দায়িত্বশীল। কর্তৃত্ব ও সম্মান।",
    "মূলা": "মূল অনুসন্ধানী, গভীর জ্ঞানী, পরিবর্তনের শক্তি রাখে। গবেষণা ও আধ্যাত্মিকতা।",
    "পূর্বাষাঢা": "অজেয় মানসিকতা, আশাবাদী, জয়ের আকাঙ্ক্ষা প্রবল। সংগ্রামী।",
    "উত্তরাষাঢা": "স্থিতিশীল, ন্যায়পরায়ণ, দীর্ঘমেয়াদী সাফল্যের অধিকারী। ধৈর্যশীল।",
    "শ্রবণা": "শ্রবণশক্তি প্রখর, জ্ঞানার্জনে আগ্রহী, ধার্মিক। শিক্ষকতা ও উপদেশ।",
    "ধনিষ্ঠা": "ধন-সম্পদ অর্জনে দক্ষ, সঙ্গীতপ্রিয়, উদ্যমী। সংগীত ও ব্যবসা।",
    "শতভিষা": "রহস্যময়, চিকিৎসা ও গবেষণায় আগ্রহী, একাকীত্ব প্রিয়। হিলিং ক্ষমতা।",
    "পূর্বভাদ্রপদ": "আধ্যাত্মিক, ত্যাগী, গভীর চিন্তাশীল। দর্শন ও তপস্যা।",
    "উত্তরভাদ্রপদ": "সহনশীল, দয়ালু, সেবাপরায়ণ। মানবিকতা ও দাতব্য।",
    "রেবতী": "কোমল, লালনপালনকারী, সম্পূর্ণতা প্রিয়। সৃজনশীল ও রক্ষাকারী।"
}

DASHA_YEARS = {
    "কেতু": 7, "শুক্র": 20, "সূর্য": 6, "চন্দ্র": 10, "মঙ্গল": 7,
    "রাহু": 18, "বৃহস্পতি": 16, "শনি": 19, "বুধ": 17
}
DASHA_ORDER = ["কেতু", "শুক্র", "সূর্য", "চন্দ্র", "মঙ্গল", "রাহু", "বৃহস্পতি", "শনি", "বুধ"]


# ==================== Geocoding ====================
@st.cache_data(show_spinner=False)
def geocode_city(city_name):
    if not city_name or not city_name.strip():
        return None
    try:
        geo_resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name.strip(), "count": 1, "language": "bn"},
            timeout=8,
        )
        geo_resp.raise_for_status()
        results = geo_resp.json().get("results")
        if not results:
            return None
        place = results[0]
        lat, lon = place["latitude"], place["longitude"]
        display = ", ".join(
            filter(None, [place.get("name"), place.get("admin1"), place.get("country")])
        )

        tz_resp = requests.get(
            "https://timeapi.io/api/timezone/coordinate",
            params={"latitude": lat, "longitude": lon},
            timeout=8,
        )
        tz_offset = 5.5
        if tz_resp.ok:
            tz_data = tz_resp.json()
            offset_str = tz_data.get("currentUtcOffset", {}).get("seconds")
            if offset_str is not None:
                tz_offset = offset_str / 3600.0

        return {
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "display": display,
            "tz_offset": tz_offset
        }
    except Exception:
        return None


# ==================== Vedic Astrology Engine ====================
class VedicAstrologyEngine:
    def __init__(self):
        self.flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    def julian_day(self, year, month, day, hour, minute, tz_offset=5.5):
        utc_hour = hour + minute / 60.0 - tz_offset
        return swe.julday(year, month, day, utc_hour)

    def get_ayanamsa(self, jd):
        return swe.get_ayanamsa_ut(jd)

    def get_planet_data(self, jd, planet_id, name_bn):
        result, flag = swe.calc_ut(jd, planet_id, self.flags)
        lon = result[0] % 360
        speed = result[3]
        is_retro = speed < 0

        if name_bn == "কেতু":
            lon = (lon + 180) % 360
            is_retro = True

        rashi_idx = int(lon // 30)
        degree_in_sign = lon % 30

        nak_span = 360.0 / 27
        nak_idx = int(lon / nak_span)
        pada = int((lon % nak_span) / (nak_span / 4)) + 1
        nak_bn, nak_en, nak_lord = NAKSHATRAS[nak_idx]

        return {
            "name": name_bn,
            "longitude": round(lon, 4),
            "rashi_bn": RASHIS_BN[rashi_idx],
            "rashi_en": RASHIS_EN[rashi_idx],
            "degree": round(degree_in_sign, 2),
            "nakshatra_bn": nak_bn,
            "nakshatra_en": nak_en,
            "pada": pada,
            "nak_lord": nak_lord,
            "retrograde": is_retro,
            "speed": round(speed, 4)
        }

    def get_lagna(self, jd, lat, lon):
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', self.flags)
        lagna_lon = ascmc[0] % 360

        rashi_idx = int(lagna_lon // 30)
        degree_in_sign = lagna_lon % 30

        nak_span = 360.0 / 27
        nak_idx = int(lagna_lon / nak_span)
        pada = int((lagna_lon % nak_span) / (nak_span / 4)) + 1
        nak_bn, nak_en, nak_lord = NAKSHATRAS[nak_idx]

        return {
            "longitude": round(lagna_lon, 4),
            "rashi_bn": RASHIS_BN[rashi_idx],
            "rashi_en": RASHIS_EN[rashi_idx],
            "degree": round(degree_in_sign, 2),
            "nakshatra_bn": nak_bn,
            "nakshatra_en": nak_en,
            "pada": pada,
            "nak_lord": nak_lord,
            "cusps": [round(c % 360, 2) for c in cusps[1:13]]
        }

    def get_vimshottari_dasha(self, moon_lon, birth_jd):
        nak_span = 360.0 / 27
        nak_idx = int(moon_lon / nak_span)
        nak_lord = NAKSHATRAS[nak_idx][2]

        fraction_left = 1 - ((moon_lon % nak_span) / nak_span)
        years_left = DASHA_YEARS[nak_lord] * fraction_left

        dasha_list = []
        current_lord = nak_lord
        start_jd = birth_jd
        start_idx = DASHA_ORDER.index(current_lord)

        for i in range(9):
            lord = DASHA_ORDER[(start_idx + i) % 9]
            years = DASHA_YEARS[lord] if i > 0 else years_left
            end_jd = start_jd + years * 365.25
            dasha_list.append({
                "lord": lord,
                "years": round(years, 2),
                "start_jd": start_jd,
                "end_jd": end_jd
            })
            start_jd = end_jd

        now_jd = swe.julday(datetime.now().year, datetime.now().month, datetime.now().day, 12)
        current = None
        for d in dasha_list:
            if d["start_jd"] <= now_jd <= d["end_jd"]:
                current = d
                break

        return dasha_list, current

    def calculate_full_chart(self, year, month, day, hour, minute, lat, lon, tz_offset=5.5):
        jd = self.julian_day(year, month, day, hour, minute, tz_offset)
        ayanamsa = self.get_ayanamsa(jd)

        planets = {}
        for name_bn, pid in PLANETS.items():
            planets[name_bn] = self.get_planet_data(jd, pid, name_bn)

        lagna = self.get_lagna(jd, lat, lon)
        moon_lon = planets["চন্দ্র"]["longitude"]
        dashas, current_dasha = self.get_vimshottari_dasha(moon_lon, jd)

        return {
            "jd": jd,
            "ayanamsa": round(ayanamsa, 4),
            "planets": planets,
            "lagna": lagna,
            "dashas": dashas,
            "current_dasha": current_dasha,
            "moon_nakshatra": planets["চন্দ্র"]["nakshatra_bn"],
            "moon_pada": planets["চন্দ্র"]["pada"]
        }


# ==================== Page Config & Styling ====================
st.set_page_config(
    page_title="কসমিক ক্যাম্পাস - গভীর জ্যোতিষ",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tiro+Bangla&family=Baloo+Da+2:wght@500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Tiro Bangla', serif; }

    .stApp {
        background: radial-gradient(circle at 10% 0%, #1b1330 0%, #0c0817 45%, #08060f 100%);
        color: #f1e9ff;
    }

    h1, h2, h3, .cc-title { font-family: 'Baloo Da 2', sans-serif; }

    .cc-hero {
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #2a1a4a 0%, #170f2e 100%);
        border: 1px solid #4b3a7a;
        margin-bottom: 1.4rem;
    }
    .cc-hero h1 {
        margin: 0;
        font-size: 2.1rem;
        color: #f4c95d;
    }
    .cc-hero p { margin: 0.35rem 0 0 0; color: #c9bce8; font-size: 0.98rem; }

    .cc-card {
        background: #161027;
        border: 1px solid #362853;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
    }

    div[data-testid="stMetric"] {
        background: #1c1433;
        border: 1px solid #3d2e63;
        border-radius: 12px;
        padding: 0.8rem 1rem 0.5rem 1rem;
    }
    div[data-testid="stMetricLabel"] { color: #c9bce8; }
    div[data-testid="stMetricValue"] { color: #f4c95d; }

    .stButton > button {
        background: linear-gradient(135deg, #f4c95d 0%, #e0a132 100%);
        color: #241606;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ffd873 0%, #eeb046 100%);
        color: #241606;
    }

    section[data-testid="stSidebar"] {
        background: #0f0a1d;
        border-right: 1px solid #2c2145;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cc-hero">
    <h1>✨ কসমিক ক্যাম্পাস</h1>
    <p>Swiss Ephemeris + Lahiri Ayanamsa • পেশাদার স্তরের বৈদিক জ্যোতিষ গণনা</p>
</div>
""", unsafe_allow_html=True)


# ==================== Session State ====================
if "geo" not in st.session_state:
    st.session_state.geo = None
if "chart" not in st.session_state:
    st.session_state.chart = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "life_steps" not in st.session_state:
    st.session_state.life_steps = []
if "life_step_index" not in st.session_state:
    st.session_state.life_step_index = 0


# ==================== Input Form ====================
st.markdown('<div class="cc-card">', unsafe_allow_html=True)
st.subheader("📝 জন্ম বিবরণ")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("আপনার নাম", "আশিম")
    birth_date = st.date_input(
        "জন্ম তারিখ",
        value=date(1976, 6, 6),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        format="DD-MM-YYYY",
    )
    birth_time = st.time_input("জন্ম সময়", value=dtime(10, 30))
    gender = st.radio("লিঙ্গ", ["পুরুষ", "মহিলা"], horizontal=True)

with col2:
    city_query = st.text_input("জন্মস্থান (শহরের নাম লিখুন)", "Jalpaiguri")
    find_col, _ = st.columns([1, 2])
    with find_col:
        find_place = st.button("📍 স্থান খুঁজুন")

    if find_place:
        with st.spinner("স্থান খোঁজা হচ্ছে..."):
            result = geocode_city(city_query)
        if result:
            st.session_state.geo = result
            st.success(f"✅ {result['display']} পাওয়া গেছে")
        else:
            st.error("দুঃখিত, এই নামে কোনো স্থান পাওয়া যায়নি। নিচে হাতে বসিয়ে দিন।")

    geo = st.session_state.geo
    default_lat = geo["lat"] if geo else 26.5333
    default_lon = geo["lon"] if geo else 88.7333
    default_tz = geo["tz_offset"] if geo else 5.5

    lat = st.number_input("অক্ষাংশ (Latitude)", value=float(default_lat), format="%.4f")
    lon = st.number_input("দ্রাঘিমাংশ (Longitude)", value=float(default_lon), format="%.4f")
    tz_offset = st.number_input("টাইমজোন অফসেট (IST = 5.5)", value=float(default_tz), step=0.5)
    blood_group = st.selectbox(
        "রক্তের গ্রুপ (ঐচ্ছিক)",
        ["জানা নেই", "B+", "A+", "O+", "AB+", "B-", "A-", "O-", "AB-"]
    )

st.markdown('</div>', unsafe_allow_html=True)

calc_clicked = st.button("🚀 সম্পূর্ণ কুণ্ডলী গণনা করুন", type="primary")

if calc_clicked:
    try:
        year, month, day = birth_date.year, birth_date.month, birth_date.day
        hour, minute = birth_time.hour, birth_time.minute

        engine = VedicAstrologyEngine()
        chart = engine.calculate_full_chart(year, month, day, hour, minute, lat, lon, tz_offset)

        st.session_state.chart = chart
        st.session_state.name = name
        st.session_state.blood_group = blood_group
        st.session_state.gender = gender
        st.session_state.birth_date = birth_date

        st.success("✅ গণনা সফলভাবে সম্পন্ন হয়েছে! (Swiss Ephemeris + Lahiri)")
    except Exception as e:
        st.error(f"গণনায় ত্রুটি হয়েছে: {e}")


# ==================== Results Display ====================
chart = st.session_state.chart
if chart:
    disp_name = st.session_state.get("name", "আপনি")
    st.header(f"📌 {disp_name}-এর সম্পূর্ণ কুণ্ডলী")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("লগ্ন (Ascendant)", f"{chart['lagna']['rashi_bn']} {chart['lagna']['degree']}°")
        st.caption(f"নক্ষত্র: {chart['lagna']['nakshatra_bn']} (পাদ {chart['lagna']['pada']})")
    with c2:
        st.metric("চন্দ্র নক্ষত্র", f"{chart['moon_nakshatra']} (পাদ {chart['moon_pada']})")
        st.caption(f"রাশি: {chart['planets']['চন্দ্র']['rashi_bn']}")
    with c3:
        st.metric("অয়নাংশ (Lahiri)", f"{chart['ayanamsa']}°")
        if chart['current_dasha']:
            st.caption(f"বর্তমান মহাদশা: **{chart['current_dasha']['lord']}**")

    char = NAKSHATRA_CHARACTER.get(chart['moon_nakshatra'], "বিশ্লেষণ চলছে...")
    st.info(f"**স্বভাব চরিত্র ({chart['moon_nakshatra']}):** {char}")

    st.subheader("🪐 গ্রহসমূহের অবস্থান (Sidereal / Lahiri)")
    planet_data = []
    for p_name, p in chart["planets"].items():
        retro = "⏪ R" if p["retrograde"] else ""
        planet_data.append({
            "গ্রহ": p_name,
            "রাশি": p["rashi_bn"],
            "ডিগ্রি": f"{p['degree']}°",
            "নক্ষত্র": f"{p['nakshatra_bn']} (পাদ {p['pada']})",
            "নক্ষত্র লর্ড": p["nak_lord"],
            "রেট্রো": retro,
            "লংগিচিউড": f"{p['longitude']}°"
        })
    st.dataframe(planet_data, use_container_width=True, hide_index=True)

    if chart['current_dasha']:
        st.subheader("⏳ বিংশোত্তরী মহাদশা")
        st.write(
            f"**বর্তমান মহাদশা:** {chart['current_dasha']['lord']} "
            f"({chart['current_dasha']['years']} বছরের মধ্যে চলমান)"
        )
        with st.expander("সম্পূর্ণ মহাদশা তালিকা দেখুন"):
            for d in chart["dashas"]:
                sj = swe.revjul(d["start_jd"])
                ej = swe.revjul(d["end_jd"])
                st.write(
                    f"- **{d['lord']}**: "
                    f"{sj[2]:02d}-{sj[1]:02d}-{sj[0]} → "
                    f"{ej[2]:02d}-{ej[1]:02d}-{ej[0]} "
                    f"({d['years']} বছর)"
                )

    bg = st.session_state.get("blood_group", "জানা নেই")
    st.info(
        f"💡 **স্বাস্থ্য টিপস:** নিয়মিত প্রাণায়াম, সূর্য নমস্কার ও পর্যাপ্ত ঘুম রাখুন। "
        f"আপনার নক্ষত্র লর্ড **{chart['planets']['চন্দ্র']['nak_lord']}** গ্রহকে শক্তিশালী রাখার চেষ্টা করুন।"
    )
else:
    st.info("উপরে জন্ম বিবরণ পূরণ করে **কুণ্ডলী গণনা করুন** বাটনে চাপ দিন।")


# ==================== Life Financial Module Integration ====================
st.markdown("---")
st.subheader("📊 জীবনচক্র ও পারিবারিক অর্থনীতি বিশ্লেষণ (বয়স ১-৬০)")

if st.button("🔍 জীবনচক্র বিশ্লেষণ শুরু করুন"):
    if chart and "birth_date" in st.session_state:
        st.session_state.life_steps = generate_life_financial_steps(
            name=st.session_state.get("name", "আপনি"),
            dob=st.session_state.birth_date,
            chart=chart
        )
        st.session_state.life_step_index = 0
    else:
        st.warning("আগে কুণ্ডলী গণনা করুন।")

steps = st.session_state.life_steps
if steps:
    for i in range(st.session_state.life_step_index + 1):
        with st.chat_message("assistant"):
            st.markdown(f"**{steps[i]['title']}**")
            st.markdown(steps[i]["content"])

    if st.session_state.life_step_index < len(steps) - 1:
        if st.button("➡️ পরবর্তী ধাপ"):
            st.session_state.life_step_index += 1
            st.rerun()
    else:
        st.success("✅ সম্পূর্ণ জীবনচক্র বিশ্লেষণ সম্পন্ন।")


# ==================== Chat System ====================
st.markdown("---")
st.subheader("💬 জ্যোতিষ প্রশ্ন করুন (চার্ট ভিত্তিক উত্তর)")
st.caption("দশা, বিয়ে, ক্যারিয়ার, স্বাস্থ্য, অর্থ, শিক্ষা, সন্তান, ভ্রমণ — যেকোনো প্রশ্ন করতে পারেন।")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def house_lord_note(chart, house_topic_planets):
    notes = []
    for p in house_topic_planets:
        if p in chart["planets"]:
            pd = chart["planets"][p]
            retro = " (বক্রী)" if pd["retrograde"] else ""
            notes.append(f"{p} আছে {pd['rashi_bn']} রাশিতে{retro}")
    return "; ".join(notes)


def generate_reply(user_prompt, chart, user_name, gender):
    if not chart:
        return (
            "প্রথমে উপরে আপনার জন্ম তথ্য দিয়ে **কুণ্ডলী গণনা** করুন। "
            "তারপর প্রশ্ন করলে আমি আপনার চার্টের উপর ভিত্তি করে উত্তর দেব।"
        )

    moon_nak = chart["moon_nakshatra"]
    lagna = chart["lagna"]["rashi_bn"]
    current_dasha = chart["current_dasha"]["lord"] if chart["current_dasha"] else "অজানা"
    char = NAKSHATRA_CHARACTER.get(moon_nak, "")
    p = chart["planets"]
    return f"""আপনার প্রশ্ন: {user_prompt}

নাম: {user_name}
লিঙ্গ: {gender}
লগ্ন: {lagna}
চন্দ্র নক্ষত্র: {moon_nak}
বর্তমান দশা: {current_dasha}

এই মুহূর্তে উত্তর তৈরির মূল অংশ অনুপস্থিত। তাই সাময়িকভাবে এই তথ্য দেখানো হচ্ছে।
"""
# ================= Chat Input & Execution =================
user_name = st.session_state.get("user_name", "ব্যবহারকারী")
gender = st.session_state.get("gender", "উল্লেখ নেই")
if user_prompt := st.chat_input("আপনার প্রশ্ন এখানে লিখুন..."):
  if "messages" not in st.session_state:
    st.session_state.messages = []
    
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.markdown(user_prompt)

  with st.chat_message("assistant"):
    with st.spinner("উত্তর তৈরি করা হচ্ছে..."):
      reply = generate_reply(
    user_prompt, chart, user_name, gender
      )
        
      st.markdown(reply)
      st.session_state.messages.append({"role": "assistant", "content": reply})
        
