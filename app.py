import streamlit as st
import swisseph as swe
import requests
from datetime import datetime, date, time as dtime

# ==================== পেজ সেটআপ ====================
st.set_page_config(page_title="রহস্য বেদা", page_icon="🔮")

# ==================== Swiss Ephemeris সেটআপ ====================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)

# ==================== ধ্রুবক ====================
RASHIS = [
    "মেষ", "বৃষ", "মিথুন", "কর্কট", "সিংহ", "কন্যা",
    "তুলা", "বৃশ্চিক", "ধনু", "মকর", "কুম্ভ", "মীন",
]

NAKSHATRAS = [
    "অশ্বিনী", "ভরণী", "কৃত্তিকা", "রোহিণী", "মৃগশিরা", "আর্দ্রা",
    "পুনর্বসু", "পুষ্যা", "অশ্লেষা", "মঘা", "পূর্বফাল্গুনী", "উত্তরফাল্গুনী",
    "হস্তা", "চিত্রা", "স্বাতী", "বিশাখা", "অনুরাধা", "জ্যেষ্ঠা",
    "মূলা", "পূর্বাষাঢ়া", "উত্তরাষাঢ়া", "শ্রবণা", "ধনিষ্ঠা", "শতভিষা",
    "পূর্বভাদ্রপদ", "উত্তরভাদ্রপদ", "রেবতী",
]

# কয়েকটি পরিচিত শহরের অক্ষাংশ/দ্রাঘিমাংশ (নাম: (lat, lon))
CITIES = {
    "শিলিগুড়ি": (26.7271, 88.3953),
    "জলপাইগুড়ি": (26.5167, 88.7333),
    "কলকাতা": (22.5726, 88.3639),
    "দিল্লি": (28.6139, 77.2090),
    "মুম্বাই": (19.0760, 72.8777),
    "ঢাকা": (23.8103, 90.4125),
    "চেন্নাই": (13.0827, 80.2707),
    "গুয়াহাটি": (26.1445, 91.7362),
}
IST_OFFSET = 5.5  # ভারতীয় সময় (UTC+5:30)


# ==================== গণনার ফাংশন ====================
def calculate_chart(dob: date, tob: dtime, lat: float, lon: float, tz: float = IST_OFFSET):
    """জন্মছকের বেসিক তথ্য হিসাব করে ফেরত দেয়।"""
    local_hour = tob.hour + tob.minute / 60 + tob.second / 3600
    ut_hour = local_hour - tz
    jd = swe.julday(dob.year, dob.month, dob.day, ut_hour)

    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    sun = swe.calc_ut(jd, swe.SUN, flags)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, flags)[0][0]

    # লগ্ন (নিরয়ন)
    houses, ascmc = swe.houses_ex(jd, lat, lon, b"P", swe.FLG_SIDEREAL)
    lagna = ascmc[0]

    nak_size = 360 / 27
    nak_index = int(moon // nak_size)
    pada = int((moon % nak_size) // (nak_size / 4)) + 1

    return {
        "sun_rashi": RASHIS[int(sun // 30)],
        "moon_rashi": RASHIS[int(moon // 30)],
        "lagna": RASHIS[int(lagna // 30)],
        "nakshatra": NAKSHATRAS[nak_index],
        "pada": pada,
    }


# ==================== AI (Gemini) ====================
def ask_ai(question: str, chart: dict, birth_info: str) -> str:
    """জন্মছকের তথ্যসহ প্রশ্ন Gemini API-তে পাঠায়।"""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        return "⚠️ API key পাওয়া যায়নি। Streamlit Secrets-এ GEMINI_API_KEY যোগ করুন।"

    context = (
        f"জন্মের তথ্য: {birth_info}\n"
        f"সূর্য রাশি: {chart['sun_rashi']}\n"
        f"চন্দ্র রাশি: {chart['moon_rashi']}\n"
        f"লগ্ন: {chart['lagna']}\n"
        f"নক্ষত্র: {chart['nakshatra']} (পাদ {chart['pada']})\n"
    )
    system_prompt = (
        "তুমি 'রহস্য বেদা', একজন বন্ধুত্বপূর্ণ বৈদিক জ্যোতিষ সহকারী। "
        "সবসময় সহজ বাংলায় উত্তর দাও। নিচের জন্মছকের তথ্য ব্যবহার করে ব্যবহারকারীর প্রশ্নের উত্তর দাও। "
        "উত্তর ছোট ও পরিষ্কার রাখো। স্বাস্থ্য, আইন বা বিনিয়োগ নিয়ে নিশ্চিত ভবিষ্যদ্বাণী কোরো না।\n\n"
        + context
    )

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": system_prompt + "\nপ্রশ্ন: " + question}]}]
    }
    try:
        r = requests.post(url, json=payload, timeout=40)
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ উত্তর আনতে সমস্যা হয়েছে: {e}"


# ==================== UI ====================
st.title("🔮 রহস্য বেদা")
st.caption("জন্মতথ্য দিন, রাশি-নক্ষত্র দেখুন, তারপর প্রশ্ন করুন।")

# --- ইনপুট ---
col1, col2 = st.columns(2)
with col1:
    dob = st.date_input(
        "জন্ম তারিখ",
        value=date(2000, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
    )
with col2:
    tob = st.time_input("জন্ম সময়", value=dtime(9, 0))

city = st.selectbox("জন্মস্থান", list(CITIES.keys()))

if st.button("🔍 দেখুন", use_container_width=True):
    lat, lon = CITIES[city]
    st.session_state.chart = calculate_chart(dob, tob, lat, lon)
    st.session_state.birth_info = f"{dob.strftime('%d/%m/%Y')}, {tob.strftime('%I:%M %p')}, {city}"
    st.session_state.messages = []  # নতুন ছকে পুরোনো চ্যাট মুছে দাও

# --- ফলাফল ---
if "chart" in st.session_state:
    chart = st.session_state.chart
    st.subheader("আপনার বেসিক তথ্য")
    c1, c2 = st.columns(2)
    c1.metric("☀️ সূর্য রাশি", chart["sun_rashi"])
    c2.metric("🌙 চন্দ্র রাশি", chart["moon_rashi"])
    c3, c4 = st.columns(2)
    c3.metric("⬆️ লগ্ন", chart["lagna"])
    c4.metric("⭐ নক্ষত্র", f"{chart['nakshatra']} (পাদ {chart['pada']})")

    st.divider()
    st.subheader("💬 এর চেয়ে বেশি জানতে হলে প্রশ্ন করুন")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    question = st.chat_input("যেকোনো কিছু জিজ্ঞেস করুন...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("ভাবছি..."):
                answer = ask_ai(question, chart, st.session_state.birth_info)
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("উপরে জন্মতথ্য দিয়ে **দেখুন** বোতাম চাপুন।")
        
