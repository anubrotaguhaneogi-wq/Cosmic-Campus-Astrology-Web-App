import streamlit as st
from astropy.coordinates import get_body, EarthLocation, GeocentricTrueEcliptic
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import solar_system_ephemeris

solar_system_ephemeris.set('builtin')

# ২৭ নক্ষত্রের তালিকা (বাংলা + ইংরেজি)
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

# নক্ষত্র অনুযায়ী সাধারণ চরিত্র
NAKSHATRA_CHARACTER = {
    "অশ্বিনী": "দ্রুত কাজ করা, সাহসী, চিকিৎসা ও যাতায়াতে আগ্রহী।",
    "ভরণী": "সৃজনশীল, কঠোর পরিশ্রমী, ন্যায়পরায়ণ।",
    "কৃত্তিকা": "তেজস্বী, নেতৃত্বের গুণসম্পন্ন, পরিষ্কার-পরিচ্ছন্নতা প্রিয়।",
    "রোহিণী": "শান্ত, সৃজনশীল, স্থির মনের, সৌন্দর্য প্রিয়।",
    "মৃগশিরা": "অনুসন্ধিৎসু, কোমল স্বভাবের, শিল্প ও সঙ্গীতে আগ্রহী।",
    "আর্দ্রা": "গভীর চিন্তাশীল, আবেগপ্রবণ, পরিবর্তনপ্রিয়।",
    "পুনর্বসু": "দয়ালু, ধৈর্যশীল, পুনরুত্থানের শক্তি রাখে।",
    "পুষ্যা": "পুষ্টিকর, ধার্মিক, লালন-পালনে পারদর্শী।",
    "অশ্লেষা": "তীক্ষ্ণ বুদ্ধিসম্পন্ন, গোপনীয়তা প্রিয়, কৌশলী।",
    "মঘা": "রাজসিক, সম্মানপ্রিয়, পূর্বপুরুষের প্রতি শ্রদ্ধাশীল।",
    "পূর্বফাল্গুনী": "আনন্দপ্রিয়, সামাজিক, শিল্পকলায় দক্ষ।",
    "উত্তরফাল্গুনী": "বিশ্বস্ত, দায়িত্বশীল, স্থিতিশীল ও সহায়ক স্বভাবের।",
    "হস্তা": "দক্ষ হাতের কাজ, ব্যবসায়ী মানসিকতা, নিখুঁত কাজ করে।",
    "চিত্রা": "সৌন্দর্যবোধ সম্পন্ন, শিল্পী স্বভাবের, আকর্ষণীয় ব্যক্তিত্ব।",
    "স্বাতী": "স্বাধীনচেতা, নমনীয়, বায়ুমণ্ডলীয় ও পরিবর্তনশীল।",
    "বিশাখা": "লক্ষ্যভেদী, দ্বৈত স্বভাবের, সাফল্যের জন্য কঠোর পরিশ্রমী।",
    "অনুরাধা": "বন্ধুত্বপূর্ণ, ভক্তিমূলক, গভীর সম্পর্ক গড়ে তোলে।",
    "জ্যেষ্ঠা": "নেতৃত্বদানের ক্ষমতা, রক্ষাকারী স্বভাব, দায়িত্বশীল।",
    "মূলা": "মূল অনুসন্ধানী, গভীর জ্ঞানী, পরিবর্তনের শক্তি রাখে।",
    "পূর্বাষাঢা": "অজেয় মানসিকতা, আশাবাদী, জয়ের আকাঙ্ক্ষা প্রবল।",
    "উত্তরাষাঢা": "স্থিতিশীল, ন্যায়পরায়ণ, দীর্ঘমেয়াদী সাফল্যের অধিকারী।",
    "শ্রবণা": "শ্রবণশক্তি প্রখর, জ্ঞানার্জনে আগ্রহী, ধার্মিক।",
    "ধনিষ্ঠা": "ধন-সম্পদ অর্জনে দক্ষ, সঙ্গীতপ্রিয়, উদ্যমী।",
    "শতভিষা": "রহস্যময়, চিকিৎসা ও গবেষণায় আগ্রহী, একাকীত্ব প্রিয়।",
    "পূর্বভাদ্রপদ": "আধ্যাত্মিক, ত্যাগী, গভীর চিন্তাশীল।",
    "উত্তরভাদ্রপদ": "সহনশীল, দয়ালু, সেবাপরায়ণ।",
    "রেবতী": "কোমল, লালনপালনকারী, সম্পূর্ণতা প্রিয়।"
}

class CosmicAstrologyApp:
    def get_lahiri_ayanamsa(self, year, month=1, day=1):
        return 23.85 + (year - 2000 + (month - 1) / 12 + (day - 1) / 365.25) * (50.29 / 3600.0)
    
    def get_moon_position(self, year, month, day, hour, minute, lat, lon, tz_offset=5.5):
        utc_hour = hour - tz_offset
        utc_day = day
        if utc_hour < 0:
            utc_hour += 24
            utc_day -= 1
        elif utc_hour >= 24:
            utc_hour -= 24
            utc_day += 1
        t_str = f"{year:04d}-{month:02d}-{utc_day:02d} {int(utc_hour):02d}:{minute:02d}:00"
        t = Time(t_str, scale='utc')
        loc = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=0 * u.m)
        moon = get_body('moon', t, location=loc)
        ecl = moon.transform_to(GeocentricTrueEcliptic(obstime=t))
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
            "longitude": round(sidereal_lon, 4)
        }

# Streamlit UI Design
st.title("🌟 কসমিক ক্যাম্পাস: জ্যোতিষ বিশ্লেষণ টুল")
st.write("আপনার জন্মতারিখ ও সময় দিয়ে নক্ষত্র ও চরিত্র জেনে নিন।")

# ইনপুট ফিল্ডসমূহ
name = st.text_input("আপনার নাম", "আশিম")
dob = st.text_input("জন্ম তারিখ (DD-MM-YYYY)", "06-06-1976")
time_str = st.text_input("জন্ম সময় (যেমন: 10:30 AM)", "10:30 AM")
place = st.text_input("জন্মস্থান", "মেটেলি")
blood_group = st.selectbox("রক্তের গ্রুপ (Blood Group)", ["B+", "A+", "O+", "AB+", "B-", "A-", "O-", "AB-"])

if st.button("🚀 গণনা করুন"):
    try:
        day, month, year = map(int, dob.split("-"))
        time_part = time_str.upper().replace(" ", "")
        is_pm = "PM" in time_part
        is_am = "AM" in time_part
        time_part = time_part.replace("AM", "").replace("PM", "")
        hour, minute = map(int, time_part.split(":"))
        if is_pm and hour != 12:
            hour += 12
        if is_am and hour == 12:
            hour = 0
            
        # স্থানাঙ্ক নির্ধারণ
        if "মেটেলি" in place or "Meteli" in place or "Matiali" in place or "Matelli" in place:
            lat, lon = 26.933, 88.817
        else:
            lat, lon = 22.5726, 88.3639

        app_calc = CosmicAstrologyApp()
        trop, sid, ayan = app_calc.get_moon_position(year, month, day, hour, minute, lat, lon)
        nak = app_calc.get_nakshatra_details(sid)
        character = NAKSHATRA_CHARACTER.get(nak["nakshatra_bn"], "চরিত্র বিশ্লেষণ চলছে...")

        # ফলাফল প্রদর্শন
        st.success("গণনা সফলভাবে সম্পন্ন হয়েছে!")
        st.write(f"### 📌 ফলাফল: {name}")
        st.markdown(f"**নক্ষত্র:** {nak['nakshatra_bn']} ({nak['nakshatra_en']})")
        st.markdown(f"**পাদ:** {nak['pada']}")
        st.markdown(f"**চাঁদের দ্রাঘিমা:** {nak['longitude']}°")
        st.markdown(f"**অয়নাংশ:** {round(ayan, 4)}°")
        st.markdown(f"**স্বভাব চরিত্র:** {character}")
        
        # স্বাস্থ্য টিপস
        st.info(f"💡 **স্বাস্থ্য টিপস ({blood_group} গ্রুপ ও {nak['nakshatra_bn']} নক্ষত্র অনুযায়ী):** নিয়মিত প্রাণায়াম, হালকা ব্যায়াম ও পর্যাপ্ত ঘুম রাখলে শরীরের শক্তি ভালো থাকবে।")

    except Exception as e:
        st.error(f"গণনায় ত্রুটি দেখা দিয়েছে: {e}")
        # স্বাস্থ্য টিপস
        st.info(f"💡 **স্বাস্থ্য টিপস ({blood_group} গ্রুপ ও {nak['nakshatra_bn']} নক্ষত্র অনুযায়ী):** নিয়মিত প্রাণায়াম, হালকা ব্যায়াম ও পর্যাপ্ত ঘুম রাখলে শরীরের শক্তি ভালো থাকবে।")

    except Exception as e:
        st.error(f"গণনায় ত্রুটি দেখা দিয়েছে: {e}")

# ==========================================
# এখানে থেকে চ্যাট বা প্রশ্ন করার সিস্টেম শুরু
# ==========================================

st.markdown("---")
st.subheader("💬 জ্যোতিষ বা অন্যান্য বিষয়ে প্রশ্ন করুন")

# চ্যাট হিস্ট্রি সেভ রাখার জন্য
if "messages" not in st.session_state:
    st.session_state.messages = []

# আগের চ্যাটগুলো স্ক্রিনে দেখানোর জন্য
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# নিচে প্রশ্ন লেখার চ্যাট ইনপুট বক্স
if user_prompt := st.chat_input("আপনার প্রশ্ন এখানে লিখুন (যেমন: আমার আজকের দিনটি কেমন যাবে?)"):
    # ইউজারের মেসেজ স্ক্রিনে দেখানো এবং সেভ করা
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # এআই-এর অটোমেটিক উত্তর জেনারেট করা
    with st.chat_message("assistant"):
        with st.spinner("উত্তর তৈরি হচ্ছে..."):
            # এখানে আপনার নক্ষত্র ও নাম ব্যবহার করে ডেমো বা এআই উত্তর তৈরি হচ্ছে
            nakshatra_name = nak['nakshatra_bn'] if 'nak' in locals() and 'nakshatra_bn' in nak else "আপনার"
            user_name = name if 'name' in locals() else "গ্রাহক"
            
            ai_reply = (
                f"নমস্কার {user_name}! আপনার **{nakshatra_name}** নক্ষত্র এবং "
                f"আপনার করা প্রশ্ন ('{user_prompt}') বিশ্লেষণ করে বলছি— বর্তমান সময়টি আপনার জন্য ইতিবাচক। "
                f"ধৈর্য ও সঠিক কর্মপ্রচেষ্টা চালিয়ে যান, সাফল্য আসবে।"
            )
            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
