import streamlit as st
import swisseph as swe
from datetime import datetime, timedelta
import math

# ==================== Swiss Ephemeris Setup ====================
swe.set_ephe_path(None)  # Built-in ephemeris
swe.set_sid_mode(swe.SIDM_LAHIRI)  # Lahiri / Chitrapaksha Ayanamsa

# ==================== Constants ====================
PLANETS = {
    "সূর্য": swe.SUN,
    "চন্দ্র": swe.MOON,
    "মঙ্গল": swe.MARS,
    "বুধ": swe.MERCURY,
    "বৃহস্পতি": swe.JUPITER,
    "শুক্র": swe.VENUS,
    "শনি": swe.SATURN,
    "রাহু": swe.TRUE_NODE,   # True Node (more accurate for Vedic)
    "কেতু": swe.TRUE_NODE,   # Will invert
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
    "অশ্বিনী": "দ্রুত কাজ করা, সাহসী, চিকিৎসা ও যাতায়াতে আগ্রহী। নেতৃত্বের গুণ আছে।",
    "ভরণী": "সৃজনশীল, কঠোর পরিশ্রমী, ন্যায়পরায়ণ। শিল্প ও সৌন্দর্য প্রিয়।",
    "কৃত্তিকা": "তেজস্বী, নেতৃত্বের গুণসম্পন্ন, পরিষ্কার-পরিচ্ছন্নতা প্রিয়। তীক্ষ্ণ বুদ্ধি।",
    "রোহিণী": "শান্ত, সৃজনশীল, স্থির মনের, সৌন্দর্য প্রিয়। লক্ষ্মীর আশীর্বাদ।",
    "মৃগশিরা": "অনুসন্ধিৎসু, কোমল স্বভাবের, শিল্প ও সঙ্গীতে আগ্রহী। পরিভ্রমণ প্রিয়।",
    "আর্দ্রা": "গভীর চিন্তাশীল, আবেগপ্রবণ, পরিবর্তনপ্রিয়। তীব্র অনুভূতিসম্পন্ন।",
    "পুনর্বসু": "দয়ালু, ধৈর্যশীল, পুনরুত্থানের শক্তি রাখে। শিক্ষা ও পরামর্শে দক্ষ।",
    "পুষ্যা": "পুষ্টিকর, ধার্মিক, লালন-পালনে পারদর্শী। রাজযোগের সম্ভাবনা।",
    "অশ্লেষা": "তীক্ষ্ণ বুদ্ধিসম্পন্ন, গোপনীয়তা প্রিয়, কৌশলী। গবেষণায় দক্ষ।",
    "মঘা": "রাজসিক, সম্মানপ্রিয়, পূর্বপুরুষের প্রতি শ্রদ্ধাশীল। কর্তৃত্বপূর্ণ।",
    "পূর্বফাল্গুনী": "আনন্দপ্রিয়, সামাজিক, শিল্পকলায় দক্ষ। ভোগ ও বিলাসিতা প্রিয়।",
    "উত্তরফাল্গুনী": "বিশ্বস্ত, দায়িত্বশীল, স্থিতিশীল ও সহায়ক স্বভাবের। পরিবারকেন্দ্রিক।",
    "হস্তা": "দক্ষ হাতের কাজ, ব্যবসায়ী মানসিকতা, নিখুঁত কাজ করে। কারিগরি দক্ষতা।",
    "চিত্রা": "সৌন্দর্যবোধ সম্পন্ন, শিল্পী স্বভাবের, আকর্ষণীয় ব্যক্তিত্ব। ডিজাইন ও ফ্যাশন।",
    "স্বাতী": "স্বাধীনচেতা, নমনীয়, বায়ুমণ্ডলীয় ও পরিবর্তনশীল। ব্যবসায় সফল।",
    "বিশাখা": "লক্ষ্যভেদী, দ্বৈত স্বভাবের, সাফল্যের জন্য কঠোর পরিশ্রমী। উচ্চাকাঙ্ক্ষী।",
    "অনুরাধা": "বন্ধুত্বপূর্ণ, ভক্তিমূলক, গভীর সম্পর্ক গড়ে তোলে। সংগঠন ক্ষমতা।",
    "জ্যেষ্ঠা": "নেতৃত্বদানের ক্ষমতা, রক্ষাকারী স্বভাব, দায়িত্বশীল। কর্তৃত্ব ও সম্মান।",
    "মূলা": "মূল অনুসন্ধানী, গভীর জ্ঞানী, পরিবর্তনের শক্তি রাখে। গবেষণা ও আধ্যাত্মিকতা।",
    "পূর্বাষাঢা": "অজেয় মানসিকতা, আশাবাদী, জয়ের আকাঙ্ক্ষা প্রবল। সংগ্রামী।",
    "উত্তরাষাঢা": "স্থিতিশীল, ন্যায়পরায়ণ, দীর্ঘমেয়াদী সাফল্যের অধিকারী। ধৈর্যশীল।",
    "শ্রবণা": "শ্রবণশক্তি প্রখর, জ্ঞানার্জনে আগ্রহী, ধার্মিক। শিক্ষকতা ও উপদেশ।",
    "ধনিষ্ঠা": "ধন-সম্পদ অর্জনে দক্ষ, সঙ্গীতপ্রিয়, উদ্যমী। সংগীত ও ব্যবসা।",
    "শতভিষা": "রহস্যময়, চিকিৎসা ও গবেষণায় আগ্রহী, একাকীত্ব প্রিয়। হিলিং ক্ষমতা।",
    "পূর্বভাদ্রপদ": "আধ্যাত্মিক, ত্যাগী, গভীর চিন্তাশীল। দর্শন ও তপস্যা।",
    "উত্তরভাদ্রপদ": "সহনশীল, দয়ালু, সেবাপরায়ণ। মানবিকতা ও দাতব্য।",
    "রেবতী": "কোমল, লালনপালনকারী, সম্পূর্ণতা প্রিয়। সৃজনশীল ও রক্ষাকারী।"
}

# Vimshottari Dasha years
DASHA_YEARS = {
    "কেতু": 7, "শুক্র": 20, "সূর্য": 6, "চন্দ্র": 10, "মঙ্গল": 7,
    "রাহু": 18, "বৃহস্পতি": 16, "শনি": 19, "বুধ": 17
}
DASHA_ORDER = ["কেতু", "শুক্র", "সূর্য", "চন্দ্র", "মঙ্গল", "রাহু", "বৃহস্পতি", "শনি", "বুধ"]

# ==================== Core Calculation Class ====================
class VedicAstrologyEngine:
    def __init__(self):
        self.flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    def julian_day(self, year, month, day, hour, minute, tz_offset=5.5):
        """Convert local time to Julian Day (UT)"""
        utc_hour = hour + minute / 60.0 - tz_offset
        return swe.julday(year, month, day, utc_hour)

    def get_ayanamsa(self, jd):
        return swe.get_ayanamsa_ut(jd)

    def get_planet_data(self, jd, planet_id, name_bn):
        result, flag = swe.calc_ut(jd, planet_id, self.flags)
        lon = result[0] % 360
        speed = result[3]
        is_retro = speed < 0

        # For Ketu: opposite of Rahu
        if name_bn == "কেতু":
            lon = (lon + 180) % 360
            is_retro = True  # Nodes are always retrograde in motion sense

        rashi_idx = int(lon // 30)
        degree_in_sign = lon % 30

        # Nakshatra
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
        """Calculate Ascendant (Lagna)"""
        # Houses using Placidus (common) or Whole Sign
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', self.flags)  # Placidus
        lagna_lon = ascmc[0] % 360  # Ascendant

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
        """Calculate current Mahadasha based on Moon's nakshatra"""
        nak_span = 360.0 / 27
        nak_idx = int(moon_lon / nak_span)
        nak_lord = NAKSHATRAS[nak_idx][2]

        # Balance of Dasha at birth
        fraction_left = 1 - ((moon_lon % nak_span) / nak_span)
        years_left = DASHA_YEARS[nak_lord] * fraction_left

        # Build timeline
        dasha_list = []
        current_lord = nak_lord
        start_jd = birth_jd

        # Find starting index
        start_idx = DASHA_ORDER.index(current_lord)

        for i in range(9):  # Full cycle
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

        # Current dasha
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

# ==================== Streamlit UI ====================
st.set_page_config(page_title="কসমিক ক্যাম্পাস - গভীর জ্যোতিষ", page_icon="🌟", layout="wide")
st.title("🌟 কসমিক ক্যাম্পাস: গভীর জ্যোতিষ বিশ্লেষণ টুল")
st.caption("Swiss Ephemeris + Lahiri Ayanamsa | পেশাদার স্তরের গণনা")

# Input Section
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("আপনার নাম", "আশিম")
    dob = st.text_input("জন্ম তারিখ (DD-MM-YYYY)", "06-06-1976")
    time_str = st.text_input("জন্ম সময় (যেমন: 10:30 AM)", "10:30 AM")
with col2:
    place = st.text_input("জন্মস্থান", "মেটেলি")
    lat = st.number_input("অক্ষাংশ (Latitude)", value=26.933, format="%.4f")
    lon = st.number_input("দ্রাঘিমাংশ (Longitude)", value=88.817, format="%.4f")
    blood_group = st.selectbox("রক্তের গ্রুপ", ["B+", "A+", "O+", "AB+", "B-", "A-", "O-", "AB-"])

tz_offset = st.number_input("টাইমজোন অফসেট (IST = 5.5)", value=5.5, step=0.5)

if st.button("🚀 সম্পূর্ণ কুণ্ডলী গণনা করুন", type="primary"):
    try:
        day, month, year = map(int, dob.split("-"))

time_part = time_str.upper().replace(" ", "").replace(".", ":")

is_pm = "PM" in time_part
is_am = "AM" in time_part

time_part = time_part.replace("AM", "").replace("PM", "")

parts = time_part.split(":")
hour = int(parts[0])
minute = int(parts[1]) if len(parts) > 1 else 0

if is_pm and hour != 12:
    hour += 12
elif is_am and hour == 12:
    hour = 0
            hour = 0

        engine = VedicAstrologyEngine()
        chart = engine.calculate_full_chart(year, month, day, hour, minute, lat, lon, tz_offset)

        # Save to session
        st.session_state.chart = chart
        st.session_state.name = name
        st.session_state.blood_group = blood_group

        st.success("✅ গণনা সফলভাবে সম্পন্ন হয়েছে! (Swiss Ephemeris + Lahiri)")

        # ===== Results Display =====
        st.header(f"📌 {name}-এর সম্পূর্ণ কুণ্ডলী")

        # Lagna & Moon
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("লগ্ন (Ascendant)", f"{chart['lagna']['rashi_bn']} {chart['lagna']['degree']}°")
            st.caption(f"নক্ষত্র: {chart['lagna']['nakshatra_bn']} (পাদ {chart['lagna']['pada']})")
        with c2:
            st.metric("চন্দ্র নক্ষত্র", f"{chart['moon_nakshatra']} (পাদ {chart['moon_pada']})")
            st.caption(f"রাশি: {chart['planets']['চন্দ্র']['rashi_bn']}")
        with c3:
            st.metric("অয়নাংশ (Lahiri)", f"{chart['ayanamsa']}°")
            if chart['current_dasha']:
                st.caption(f"বর্তমান মহাদশা: **{chart['current_dasha']['lord']}**")

        # Character
        char = NAKSHATRA_CHARACTER.get(chart['moon_nakshatra'], "বিশ্লেষণ চলছে...")
        st.info(f"**স্বভাব চরিত্র ({chart['moon_nakshatra']}):** {char}")

        # Planetary Table
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

        # Current Dasha
        if chart['current_dasha']:
            st.subheader("⏳ বিংশোত্তরী মহাদশা")
            st.write(f"**বর্তমান মহাদশা:** {chart['current_dasha']['lord']} "
                     f"({chart['current_dasha']['years']} বছরের মধ্যে চলমান)")

        # Health tip
        st.info(f"💡 **স্বাস্থ্য টিপস ({blood_group} + {chart['moon_nakshatra']}):** "
                f"নিয়মিত প্রাণায়াম, সূর্য নমস্কার ও পর্যাপ্ত ঘুম রাখুন। "
                f"আপনার নক্ষত্র অনুযায়ী {chart['planets']['চন্দ্র']['nak_lord']} গ্রহের শক্তিশালী রাখুন।")

    except Exception as e:
        st.error(f"গণনায় ত্রুটি: {e}")
        st.exception(e)

# ==================== Chat System ====================
st.markdown("---")
st.subheader("💬 জ্যোতিষ প্রশ্ন করুন (চার্ট ভিত্তিক উত্তর)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("আপনার প্রশ্ন লিখুন (যেমন: আমার বর্তমান দশা কেমন? / বিয়ে কখন হবে?)"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("চার্ট বিশ্লেষণ করে উত্তর তৈরি হচ্ছে..."):
            chart = st.session_state.get("chart", None)
            user_name = st.session_state.get("name", "আপনি")

            if not chart:
                ai_reply = "প্রথমে উপরে আপনার জন্ম তথ্য দিয়ে **কুণ্ডলী গণনা** করুন। তারপর প্রশ্ন করলে আমি চার্টের উপর ভিত্তি করে উত্তর দেব।"
            else:
                moon_nak = chart["moon_nakshatra"]
                lagna = chart["lagna"]["rashi_bn"]
                current_dasha = chart["current_dasha"]["lord"] if chart["current_dasha"] else "অজানা"
                char = NAKSHATRA_CHARACTER.get(moon_nak, "")

                prompt_lower = user_prompt.lower()

                # Rule-based intelligent replies
                if any(w in prompt_lower for w in ["দশা", "মহদশা", "বর্তমান", "এখন"]):
                    ai_reply = (f"নমস্কার {user_name}! আপনার বর্তমান **{current_dasha} মহাদশা** চলছে। "
                                f"চন্দ্র নক্ষত্র **{moon_nak}** এবং লগ্ন **{lagna}**। "
                                f"{char} এই সময়ে ধৈর্য ও সঠিক কর্মপ্রচেষ্টা রাখলে ভালো ফল পাবেন।")
                elif any(w in prompt_lower for w in ["বিয়ে", "বিবাহ", "marriage", "শাদী"]):
                    ai_reply = (f"{user_name}, আপনার চন্দ্র নক্ষত্র **{moon_nak}** এবং লগ্ন **{lagna}** দেখে বলছি — "
                                f"বিবাহের সময় সাধারণত শুক্র বা বৃহস্পতির দশায় ভালো হয়। "
                                f"বর্তমান {current_dasha} দশায় সম্পর্কের বিষয়ে সতর্ক থাকুন। "
                                f"বিস্তারিত জানতে নবম ও সপ্তম ভাবের বিশ্লেষণ প্রয়োজন।")
                elif any(w in prompt_lower for w in ["চাকরি", "ক্যারিয়ার", "জব", "পেশা", "কাজ"]):
                    ai_reply = (f"{user_name}, আপনার **{moon_nak}** নক্ষত্র ও **{lagna}** লগ্ন অনুযায়ী "
                                f"ক্যারিয়ারে {chart['planets']['সূর্য']['rashi_bn']} ও {chart['planets']['শনি']['rashi_bn']} "
                                f"রাশির প্রভাব আছে। বর্তমান {current_dasha} দশায় পরিশ্রম করলে অগ্রগতি হবে।")
                elif any(w in prompt_lower for w in ["স্বাস্থ্য", "অসুস্থ", "রোগ", "health"]):
                    ai_reply = (f"আপনার রক্তের গ্রুপ ও **{moon_nak}** নক্ষত্র অনুযায়ী "
                                f"নিয়মিত যোগাভ্যাস, প্রাণায়াম ও সঠিক খাদ্যাভ্যাস রাখুন। "
                                f"চন্দ্রের অবস্থান **{chart['planets']['চন্দ্র']['rashi_bn']}**-এ থাকায় মানসিক শান্তি গুরুত্বপূর্ণ।")
                elif any(w in prompt_lower for w in ["ভাগ্য", "আজ", "আজকের", "দিন"]):
                    ai_reply = (f"আজকের দিনে আপনার **{moon_nak}** নক্ষত্রের প্রভাব ইতিবাচক। "
                                f"লগ্ন {lagna} হওয়ায় সকালের সময় ভালো। "
                                f"{current_dasha} দশা চলাকালীন ধৈর্য ধরে কাজ করুন।")
                else:
                    ai_reply = (f"নমস্কার {user_name}! আপনার চার্ট অনুযায়ী:\n\n"
                                f"- **লগ্ন:** {lagna}\n"
                                f"- **চন্দ্র নক্ষত্র:** {moon_nak} (পাদ {chart['moon_pada']})\n"
                                f"- **বর্তমান মহাদশা:** {current_dasha}\n\n"
                                f"**স্বভাব:** {char}\n\n"
                                f"আপনার প্রশ্ন '{user_prompt}' সম্পর্কে বলতে পারি — "
                                f"এই সময়টি আপনার জন্য সাধারণত ইতিবাচক। "
                                f"আরও নির্দিষ্ট প্রশ্ন করলে (দশা, বিয়ে, ক্যারিয়ার, স্বাস্থ্য) আরও গভীর উত্তর দেব।")

            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
