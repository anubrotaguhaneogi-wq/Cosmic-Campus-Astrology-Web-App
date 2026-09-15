import os
import streamlit as st
from astropy import units as u
from astropy.coordinates import EarthLocation, GeocentricTrueEcliptic, get_body
from astropy.coordinates import solar_system_ephemeris
from astropy.time import Time

solar_system_ephemeris.set('builtin')

# ==========================================
# ২৭ নক্ষত্রের তালিকা (বাংলা + ইংরেজি)
# ==========================================
NAKSHATRAS = [
    ("অশ্বিনী", "Ashwini"),
    ("ভরণী", "Bharani"),
    ("কৃত্তিকা", "Krittika"),
    ("রোহিণী", "Rohini"),
    ("মৃগশিরা", "Mrigashira"),
    ("আর্দ্রা", "Ardra"),
    ("পুনর্বসু", "Punarvasu"),
    ("পুষ্যা", "Pushya"),
    ("অশ্লেষা", "Ashlesha"),
    ("মঘা", "Magha"),
    ("পূর্বফাল্গুনী", "Purva Phalguni"),
    ("উত্তরফাল্গুনী", "Uttara Phalguni"),
    ("হস্তা", "Hasta"),
    ("চিত্রা", "Chitra"),
    ("স্বাতী", "Swati"),
    ("বিশাখা", "Vishakha"),
    ("অনুরাধা", "Anuradha"),
    ("জ্যেষ্ঠা", "Jyeshtha"),
    ("মূলা", "Mula"),
    ("পূর্বাষাঢা", "Purva Ashadha"),
    ("উত্তরাষাঢা", "Uttara Ashadha"),
    ("শ্রবণা", "Shravana"),
    ("ধনিষ্ঠা", "Dhanishta"),
    ("শতভিষা", "Shatabhisha"),
    ("পূর্বভাদ্রপদ", "Purva Bhadrapada"),
    ("উত্তরভাদ্রপদ", "Uttar Bhadrapada"),
    ("রেবতী", "Revati"),
]

NAKSHATRA_CHARACTER = {
    "অশ্বিনী": "দ্রুত কাজ করা, সাহসী, চিকিৎসা ও যাতায়াতে আগ্রহী।",
    "ভরণী": "সৃজনশীল, কঠোর পরিশ্রমী, ন্যায়পরায়ণ।",
    "কৃত্তিকা": "তেজস্বী, নেতৃত্বের গুণসম্পন্ন, পরিষ্কার-পরিচ্ছন্নতা প্রিয়।",
    "রোহিণী": "শান্ত, সৃজনশীল, স্থির মনের, সৌন্দর্য প্রিয়।",
    "মৃগশিরা": "অনুসন্ধিৎসু, কোমল স্বভাবের, শিল্প ও সঙ্গীতে আগ্রহী।",
    "আর্দ্রা": "গভীর চিন্তাশীল, আবেগপ্রবণ, পরিবর্তনপ্রিয়।",
    "পুনর্বসু": "দয়ালু, ধৈর্যশীল, পুনরুত্থানের শক্তি রাখে।",
    "পুষ্যা": "পুষ্টিকর, ধার্মিক, লালন-পালনে পারদর্শী।",
    "অশ্লেষা": "তীক্ষ্ণ বুদ্ধিসম্পন্ন, গোপনীয়তা প্রিয়, কৌশলী।",
    "মঘা": "রাজসিক, সম্মানপ্রিয়, পূর্বপুরুষের প্রতি শ্রদ্ধাশীল।",
    "পূর্বফাল্গুনী": "আনন্দপ্রিয়, সামাজিক, শিল্পকলায় দক্ষ।",
    "উত্তরফাল্গুনী": "বিশ্বস্ত, দায়িত্বশীল, স্থিতিশীল ও সহায়ক স্বভাবের।",
    "হস্তা": "দক্ষ হাতের কাজ, ব্যবসায়ী মানসিকতা, নিখুঁত কাজ করে।",
    "চিত্রা": "সৌন্দর্যবোধ সম্পন্ন, শিল্পী স্বভাবের, আকর্ষণীয় ব্যক্তিত্ব।",
    "স্বাতী": "স্বাধীনচেতা, নমনীয়, বায়ুমণ্ডলীয় ও পরিবর্তনশীল।",
    "বিশাখা": "লক্ষ্যভেদী, দ্বৈত স্বভাবের, সাফল্যের জন্য কঠোর পরিশ্রমী।",
    "অনুরাধা": "বন্ধুত্বপূর্ণ, ভক্তিমূলক, গভীর সম্পর্ক গড়ে তোলে।",
    "জ্যেষ্ঠা": "নেতৃত্বদানের ক্ষমতা, রক্ষাকারী স্বভাব, দায়িত্বশীল।",
    "মূলা": "মূল অনুসন্ধানী, গভীর জ্ঞানী, পরিবর্তনের শক্তি রাখে।",
    "পূর্বাষাঢা": "অজেয় মানসিকতা, আশাবাদী, জয়ের আকাঙ্ক্ষা প্রবল।",
    "উত্তরাষাঢা": "স্থিতিশীল, ন্যায়পরায়ণ, দীর্ঘমেয়াদী সাফল্যের অধিকারী।",
    "শ্রবণা": "শ্রবণশক্তি প্রখর, জ্ঞানার্জনে আগ্রহী, ধার্মিক।",
    "ধনিষ্ঠা": "ধন-সম্পদ অর্জনে দক্ষ, সঙ্গীতপ্রিয়, উদ্যমী।",
    "শতভিষা": "রহস্যময়, চিকিৎসা ও গবেষণায় আগ্রহী, একাকীত্ব প্রিয়।",
    "পূর্বভাদ্রপদ": "আধ্যাত্মিক, ত্যাগী, গভীর চিন্তাশীল।",
    "উত্তরভাদ্রপদ": "সহনশীল, দয়ালু, সেবাপরায়ণ।",
    "রেবতী": "কোমল, লালনপালনকারী, সম্পূর্ণতা প্রিয়।",
}

# ==========================================
# ১২ রাশির তালিকা (বাংলা + ইংরেজি)
# ==========================================
RASHIS = [
    ("মেষ", "Aries"),
    ("বৃষ", "Taurus"),
    ("মিথুন", "Gemini"),
    ("কর্কট", "Cancer"),
    ("সিংহ", "Leo"),
    ("কন্যা", "Virgo"),
    ("তুলা", "Libra"),
    ("বৃশ্চিক", "Scorpio"),
    ("ধনু", "Sagittarius"),
    ("মকর", "Capricorn"),
    ("কুম্ভ", "Aquarius"),
    ("মীন", "Pisces"),
]

# ==========================================
# বড় ভারতীয় শহরের তালিকা (lat, lon) — অফলাইন
# ==========================================
CITY_COORDS = {
    "মেটেলি": (26.933, 88.817),
    "matiali": (26.933, 88.817),
    "meteli": (26.933, 88.817),
    "জলপাইগুড়ি": (26.5167, 88.7333),
    "jalpaiguri": (26.5167, 88.7333),
    "শিলিগুড়ি": (26.7271, 88.3953),
    "siliguri": (26.7271, 88.3953),
    "কলকাতা": (22.5726, 88.3639),
    "kolkata": (22.5726, 88.3639),
    "calcutta": (22.5726, 88.3639),
    "দার্জিলিং": (27.0410, 88.2663),
    "darjeeling": (27.0410, 88.2663),
    "কোচবিহার": (26.3200, 89.4400),
    "cooch behar": (26.3200, 89.4400),
    "coochbehar": (26.3200, 89.4400),
    "আলিপুরদুয়ার": (26.4900, 89.5300),
    "alipurduar": (26.4900, 89.5300),
    "মুম্বাই": (19.0760, 72.8777),
    "mumbai": (19.0760, 72.8777),
    "bombay": (19.0760, 72.8777),
    "দিল্লি": (28.6139, 77.2090),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "চেন্নাই": (13.0827, 80.2707),
    "chennai": (13.0827, 80.2707),
    "madras": (13.0827, 80.2707),
    "ব্যাঙ্গালোর": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "হায়দ্রাবাদ": (17.3850, 78.4867),
    "hyderabad": (17.3850, 78.4867),
    "পুনে": (18.5204, 73.8567),
    "pune": (18.5204, 73.8567),
    "আহমেদাবাদ": (23.0225, 72.5714),
    "ahmedabad": (23.0225, 72.5714),
    "জয়পুর": (26.9124, 75.7873),
    "jaipur": (26.9124, 75.7873),
    "লখনউ": (26.8467, 80.9462),
    "lucknow": (26.8467, 80.9462),
    "পাটনা": (25.5941, 85.1376),
    "patna": (25.5941, 85.1376),
    "ভুবনেশ্বর": (20.2961, 85.8245),
    "bhubaneswar": (20.2961, 85.8245),
    "গুয়াহাটি": (26.1445, 91.7362),
    "guwahati": (26.1445, 91.7362),
    "রাঁচি": (23.3441, 85.3096),
    "ranchi": (23.3441, 85.3096),
    "চণ্ডীগড়": (30.7333, 76.7794),
    "chandigarh": (30.7333, 76.7794),
    "ভোপাল": (23.2599, 77.4126),
    "bhopal": (23.2599, 77.4126),
    "ইন্দোর": (22.7196, 75.8577),
    "indore": (22.7196, 75.8577),
    "নাগপুর": (21.1458, 79.0882),
    "nagpur": (21.1458, 79.0882),
    "কানপুর": (26.4499, 80.3319),
    "kanpur": (26.4499, 80.3319),
    "বারাণসী": (25.3176, 82.9739),
    "varanasi": (25.3176, 82.9739),
    "banaras": (25.3176, 82.9739),
    "অমৃতসর": (31.6340, 74.8723),
    "amritsar": (31.6340, 74.8723),
    "শ্রীনগর": (34.0837, 74.7973),
    "srinagar": (34.0837, 74.7973),
    "কোয়েম্বাটুর": (11.0168, 76.9558),
    "coimbatore": (11.0168, 76.9558),
    "কোচি": (9.9312, 76.2673),
    "kochi": (9.9312, 76.2673),
    "cochin": (9.9312, 76.2673),
    "তিরুবনন্তপুরম": (8.5241, 76.9366),
    "thiruvananthapuram": (8.5241, 76.9366),
    "বিশাখাপত্তনম": (17.6868, 83.2185),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "সুরাট": (21.1702, 72.8311),
    "surat": (21.1702, 72.8311),
    "নাসিক": (19.9975, 73.7898),
    "nashik": (19.9975, 73.7898),
    "রায়পুর": (21.2514, 81.6296),
    "raipur": (21.2514, 81.6296),
    "দেরাদুন": (30.3165, 78.0322),
    "dehradun": (30.3165, 78.0322),
    "আসানসোল": (23.6739, 86.9524),
    "asansol": (23.6739, 86.9524),
    "দুর্গাপুর": (23.5204, 87.3119),
    "durgapur": (23.5204, 87.3119),
    "মালদা": (25.0108, 88.1411),
    "malda": (25.0108, 88.1411),
    "বহরমপুর": (24.1000, 88.2500),
    "berhampore": (24.1000, 88.2500),
}

DEFAULT_COORDS = (22.5726, 88.3639)  # কলকাতা — শহর না মিললে ডিফল্ট


def find_city_coords(place: str):
  key = place.strip().lower()
  if key in CITY_COORDS:
    return CITY_COORDS[key], True
  for city_key, coords in CITY_COORDS.items():
    if city_key in key or key in city_key:
      return coords, True
  return DEFAULT_COORDS, False


# ==========================================
# জ্যোতিষ গণনার মূল ক্লাস
# ==========================================
class CosmicAstrologyApp:

  def get_lahiri_ayanamsa(self, year, month=1, day=1):
    return (
        23.85
        + (year - 2000 + (month - 1) / 12 + (day - 1) / 365.25)
        * (50.29 / 3600.0)
    )

  def _to_utc_time(self, year, month, day, hour, minute, tz_offset=5.5):
    total_minutes = hour * 60 + minute - int(tz_offset * 60)
    utc_day = day
    if total_minutes < 0:
      total_minutes += 24 * 60
      utc_day -= 1
    elif total_minutes >= 24 * 60:
      total_minutes -= 24 * 60
      utc_day += 1
    utc_hour = total_minutes // 60
    utc_minute = total_minutes % 60
    t_str = f"{year:04d}-{month:02d}-{utc_day:02d} {int(utc_hour):02d}:{int(utc_minute):02d}:00"
    return Time(t_str, scale="utc")

  def get_body_sidereal_longitude(
      self, body_name, year, month, day, hour, minute, lat, lon, tz_offset=5.5
  ):
    t = self._to_utc_time(year, month, day, hour, minute, tz_offset)
    loc = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=0 * u.m)
    body = get_body(body_name, t, location=loc)
    ecl = body.transform_to(GeocentricTrueEcliptic(obstime=t))
    tropical_lon = ecl.lon.deg % 360
    ayan = self.get_lahiri_ayanamsa(year, month, day)
    sidereal_lon = (tropical_lon - ayan) % 360
    return tropical_lon, sidereal_lon, ayan

  def get_nakshatra_details(self, sidereal_lon):
    span = 360.0 / 27
    n_index = int(sidereal_lon / span)
    pada = int((sidereal_lon % span) / (span / 4)) + 1
    name_bn, name_en = NAKSHATRAS[n_index]
    return {
        "nakshatra_bn": name_bn,
        "nakshatra_en": name_en,
        "number": n_index + 1,
        "pada": pada,
        "longitude": round(sidereal_lon, 4),
    }

  def get_rashi_details(self, sidereal_lon):
    r_index = int(sidereal_lon / 30) % 12
    name_bn, name_en = RASHIS[r_index]
    return {
        "rashi_bn": name_bn,
        "rashi_en": name_en,
        "longitude": round(sidereal_lon, 4),
    }

  def get_ascendant_sidereal(
      self, year, month, day, hour, minute, lat, lon, tz_offset=5.5
  ):
    import math

    t = self._to_utc_time(year, month, day, hour, minute, tz_offset)
    lst = t.sidereal_time("apparent", longitude=lon * u.deg).deg
    obliquity = 23.4367
    lat_rad = math.radians(lat)
    obl_rad = math.radians(obliquity)
    lst_rad = math.radians(lst)
    y = -math.cos(lst_rad)
    x = math.sin(obl_rad) * math.tan(lat_rad) + math.cos(obl_rad) * math.sin(
        lst_rad
    )
    asc_tropical = math.degrees(math.atan2(y, x)) % 360
    ayan = self.get_lahiri_ayanamsa(year, month, day)
    asc_sidereal = (asc_tropical - ayan) % 360
    return asc_sidereal


# ==========================================
# Claude API দিয়ে চ্যাট রিপ্লাই
# ==========================================
def get_claude_reply(api_key, user_prompt, context: dict):
  import anthropic

  client = anthropic.Anthropic(api_key=api_key)

  system_prompt = (
      "তুমি একজন অভিজ্ঞ বৈদিক জ্যোতিষী। ইউজারের জন্মকুণ্ডলীর তথ্য ব্যবহার করে"
      " বাংলা ভাষায়, সহজ ও উষ্ণ সুরে উত্তর দাও। জ্যোতিষের সাধারণ ব্যাখ্যা দাও, তবে"
      " কখনো নিশ্চিতভাবে ভবিষ্যদ্বাণী করবে না বা চিকিৎসা/আর্থিক সিদ্ধান্ত নিয়ে চূড়ান্ত"
      " নির্দেশ দেবে না — এগুলো একজন যোগ্য পেশাদারের কাছে পাঠাও প্রয়োজনে। উত্তর সংক্ষিপ্ত"
      " (৩-৫ বাক্য) ও প্রাসঙ্গিক রাখো।\n\n"
      f"ইউজারের তথ্য:\n"
      f"নাম: {context.get('name')}\n"
      f"নক্ষত্র: {context.get('nakshatra_bn')} ({context.get('nakshatra_en')}),"
      f" পাদ {context.get('pada')}\n"
      f"রাশি: {context.get('rashi_bn')} ({context.get('rashi_en')})\n"
      f"লগ্ন রাশি: {context.get('lagna_bn', 'জানা নেই')}\n"
      f"জন্মস্থান: {context.get('place')}\n"
  )

  message = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=500,
      system=system_prompt,
      messages=[{"role": "user", "content": user_prompt}],
  )
  return message.content[0].text


# ==========================================
# Streamlit UI
# ==========================================
st.set_page_config(page_title="কসমিক ক্যাম্পাস", page_icon="🌟")
st.title("🌟 কসমিক ক্যাম্পাস: জ্যোতিষ বিশ্লেষণ টুল")
st.write("আপনার জন্মতারিখ ও সময় দিয়ে নক্ষত্র, রাশি ও লগ্ন জেনে নিন।")

with st.sidebar:
  st.subheader("⚙️ সেটিংস")
  api_key_input = st.text_input(
      "Anthropic API Key (চ্যাটের জন্য)",
      value=os.environ.get("ANTHROPIC_API_KEY", ""),
      type="password",
      help=(
          "claude.ai/settings/keys থেকে নিতে পারেন। কী সেভ হয় না, শুধু এই সেশনে"
          " ব্যবহার হয়।"
      ),
  )

name = st.text_input("আপনার নাম", "আশিম")
dob = st.text_input("জন্ম তারিখ (DD-MM-YYYY)", "06-06-1976")
time_str = st.text_input("জন্ম সময় (যেমন: 10:30 AM)", "10:30 AM")
place = st.text_input("জন্মস্থান (যেকোনো ভারতীয় শহর)", "মেটেলি")
blood_group = st.selectbox(
    "রক্তের গ্রুপ (Blood Group)",
    ["B+", "A+", "O+", "AB+", "B-", "A-", "O-", "AB-"],
)

if st.button("🚀 গণনা করুন"):
  try:
    parts = dob.strip().split("-")
    if len(parts) != 3:
      raise ValueError(
          "তারিখ অবশ্যই DD-MM-YYYY ফরম্যাটে দিন, যেমন: 06-06-1976"
      )
    day, month, year = map(int, parts)
    if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100):
      raise ValueError("তারিখের মান সঠিক নয়। দিন/মাস/বছর যাচাই করুন।")

    time_part = time_str.upper().replace(" ", "")
    is_pm = "PM" in time_part
    is_am = "AM" in time_part
    time_part = time_part.replace("AM", "").replace("PM", "")
    time_bits = time_part.split(":")
    if len(time_bits) != 2:
      raise ValueError("সময় অবশ্যই HH:MM ফরম্যাটে দিন, যেমন: 10:30 AM")
    hour, minute = map(int, time_bits)
    if not (0 <= minute <= 59):
      raise ValueError("মিনিটের মান 0-59 এর মধ্যে হতে হবে।")
    if is_pm:
      if not (1 <= hour <= 12):
        raise ValueError("PM সময়ে ঘণ্টা 1-12 এর মধ্যে হতে হবে।")
      if hour != 12:
        hour += 12
    elif is_am:
      if not (1 <= hour <= 12):
        raise ValueError("AM সময়ে ঘণ্টা 1-12 এর মধ্যে হতে হবে।")
      if hour == 12:
        hour = 0
    else:
      if not (0 <= hour <= 23):
        raise ValueError("24-ঘণ্টা ফরম্যাটে ঘণ্টা 0-23 এর মধ্যে হতে হবে।")

    (lat, lon), matched = find_city_coords(place)
    if not matched:
      st.warning(
          f"⚠️ '{place}' শহরটি তালিকায় পাওয়া যায়নি, তাই কলকাতার স্থানাঙ্ক"
          " ব্যবহার করা হয়েছে। ফলাফল কিছুটা ভিন্ন হতে পারে।"
      )

    app_calc = CosmicAstrologyApp()

    _, moon_sid, ayan = app_calc.get_body_sidereal_longitude(
        "moon", year, month, day, hour, minute, lat, lon
    )
    nak = app_calc.get_nakshatra_details(moon_sid)
    moon_rashi = app_calc.get_rashi_details(moon_sid)

    _, sun_sid, _ = app_calc.get_body_sidereal_longitude(
        "sun", year, month, day, hour, minute, lat, lon
    )
    sun_rashi = app_calc.get_rashi_details(sun_sid)

    asc_sid = app_calc.get_ascendant_sidereal(
        year, month, day, hour, minute, lat, lon
    )
    lagna_rashi = app_calc.get_rashi_details(asc_sid)

    character = NAKSHATRA_CHARACTER.get(
        nak["nakshatra_bn"], "চরিত্র বিশ্লেষণ চলছে..."
    )

    st.session_state["last_result"] = {
        "name": name,
        "place": place,
        "nakshatra_bn": nak["nakshatra_bn"],
        "nakshatra_en": nak["nakshatra_en"],
        "pada": nak["pada"],
        "rashi_bn": moon_rashi["rashi_bn"],
        "rashi_en": moon_rashi["rashi_en"],
        "sun_rashi_bn": sun_rashi["rashi_bn"],
        "sun_rashi_en": sun_rashi["rashi_en"],
        "lagna_bn": lagna_rashi["rashi_bn"],
        "lagna_en": lagna_rashi["rashi_en"],
    }

    st.success("গণনা সফলভাবে সম্পন্ন হয়েছে!")
    st.write(f"### 📌 ফলাফল: {name}")

    col1, col2 = st.columns(2)
    with col1:
      st.markdown(f"**নক্ষত্র:** {nak['nakshatra_bn']} ({nak['nakshatra_en']})")
      st.markdown(f"**পাদ:** {nak['pada']}")
      st.markdown(
          f"**চন্দ্র রাশি:** {moon_rashi['rashi_bn']} ({moon_rashi['rashi_en']})"
      )
    with col2:
      st.markdown(
          f"**সূর্য রাশি:** {sun_rashi['rashi_bn']} ({sun_rashi['rashi_en']})"
      )
      st.markdown(
          f"**লগ্ন রাশি:** {lagna_rashi['rashi_bn']} ({lagna_rashi['rashi_en']})"
          " *(আনুমানিক)*"
      )
      st.markdown(f"**অয়নাংশ:** {round(ayan, 4)}°")

    st.markdown(f"**স্বভাব চরিত্র:** {character}")

    st.info(
        f"💡 **স্বাস্থ্য টিপস ({blood_group} গ্রুপ ও {nak['nakshatra_bn']} নক্ষত্র"
        ' অনুযায়ী):** নিয়মিত প্রাণায়াম, হালকা ব্যায়াম ও পর্যাপ্ত ঘুম'
        " রাখলে শরীরের শক্তি ভালো থাকবে।"
    )

    st.caption(
        "⚠️ লগ্ন গণনাটি একটি সরলীকৃত পদ্ধতিতে করা হয়েছে এবং আনুমানিক — নির্ভুল"
        " জন্মকুণ্ডলীর জন্য পেশাদার জ্যোতিষীর পরামর্শ নিন।"
    )

  except ValueError as ve:
    st.error(f"ইনপুট ত্রুটি: {ve}")
  except Exception as e:
    st.error(f"গণনায় ত্রুটি দেখা দিয়েছে: {e}")

# ==========================================
# চ্যাট সিস্টেম — Claude API দিয়ে
# ==========================================
st.markdown("---")
st.subheader("💬 জ্যোতিষ বা অন্যান্য বিষয়ে প্রশ্ন করুন")

if "messages" not in st.session_state:
  st.session_state.messages = []

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if user_prompt := st.chat_input(
    "আপনার প্রশ্ন এখানে লিখুন (যেমন: আমার আজকের দিনটি কেমন যাবে?)"
):
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.markdown(user_prompt)

  with st.chat_message("assistant"):
    if not api_key_input:
      reply = (
          "⚠️ চ্যাট ব্যবহার করতে বাঁ পাশের সাইডবারে আপনার Anthropic API Key দিন।"
      )
      st.markdown(reply)
    else:
      with st.spinner("উত্তর তৈরি হচ্ছে..."):
        context = st.session_state.get(
            "last_result", {"name": name, "place": place}
        )
        try:
          reply = get_claude_reply(api_key_input, user_prompt, context)
          st.markdown(reply)
        except Exception as e:
          reply = f"দুঃখিত, উত্তর আনতে সমস্যা হয়েছে: {e}"
          st.error(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
