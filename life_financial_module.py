# ============================================================
# life_financial_module.py
# কসমিক ক্যাম্পাস — বয়স ১-৬০ জীবনচক্র ও পারিবারিক অর্থনীতি মডেল
# ============================================================

from datetime import date

LIFE_PHASES = [
    {
        "range": (1, 6),
        "planet": "সূর্য",
        "planet_en": "Sun",
        "life_progression": (
            "সন্তানের স্বাস্থ্য ও ভিত্তিগত স্থিতিশীলতার উপর মূল ফোকাস। "
            "শারীরিক ও মানসিক বুনিয়াদ তৈরি হয় এই পর্যায়ে।"
        ),
        "father_income_focus": (
            "বাবার আয় (৫০% ফোকাস) এই সময়ে প্রাথমিক সংসার গঠন ও প্রথম সঞ্চয় "
            "তৈরিতে চালিকাশক্তি হিসেবে কাজ করে।"
        ),
    },
    {
        "range": (7, 12),
        "planet": "চন্দ্র",
        "planet_en": "Moon",
        "life_progression": (
            "স্কুলজীবন শুরু ও আবেগীয় বিকাশ। মানসিক স্থিতিশীলতা ও শেখার আগ্রহ "
            "গড়ে ওঠার সময়।"
        ),
        "father_income_focus": (
            "বাবার আয় বেড়ে চলা শিক্ষা ও টিউশন খরচ সামলানোর দায়িত্ব নেয়।"
        ),
    },
    {
        "range": (13, 18),
        "planet": "মঙ্গল",
        "planet_en": "Mars",
        "life_progression": (
            "উচ্চ বিদ্যালয় স্তর ও কৈশোর — শারীরিক-মানসিক পরিবর্তনের সময়।"
        ),
        "father_income_focus": (
            "বাবার আয় এই সময়ে সর্বোচ্চ ক্ষমতায় পৌঁছায়, উচ্চশিক্ষা ও বড় খরচের "
            "প্রস্তুতির জন্য।"
        ),
    },
    {
        "range": (19, 24),
        "planet": "রাহু",
        "planet_en": "Rahu",
        "life_progression": (
            "উচ্চশিক্ষা ও কর্মজীবনে প্রথম পদার্পণ। স্বাধীনতার দিকে যাত্রা শুরু।"
        ),
        "father_income_focus": (
            "বাবার সরাসরি আয়ের উপর নির্ভরতা থেকে ধীরে ধীরে যৌথ পারিবারিক "
            "তহবিল বা স্বাধীন অর্থায়নের দিকে পরিবর্তন।"
        ),
    },
    {
        "range": (25, 30),
        "planet": "বৃহস্পতি",
        "planet_en": "Jupiter",
        "life_progression": (
            "ক্যারিয়ার গঠনের পর্যায়। সন্তান ক্রমশ আত্মনির্ভরশীল হয়ে ওঠে।"
        ),
        "father_income_focus": (
            "বাবার উপর সরাসরি আর্থিক চাপ কমে আসে, সন্তান নিজের পায়ে দাঁড়ায়।"
        ),
    },
    {
        "range": (31, 36),
        "planet": "শনি",
        "planet_en": "Saturn",
        "life_progression": (
            "পেশাগত দায়িত্ব বৃদ্ধি পায়। নিজস্ব সংসার ও দায়িত্বের সূচনা।"
        ),
        "father_income_focus": (
            "মূল পারিবারিক আর্থিক দায়িত্ব এখন ধীরে ধীরে সন্তানের দিকে সরে যায়।"
        ),
    },
    {
        "range": (37, 42),
        "planet": "বুধ",
        "planet_en": "Mercury",
        "life_progression": (
            "ব্যবসা/ক্যারিয়ারে স্থিতিশীলতা অর্জন।"
        ),
        "father_income_focus": (
            "দীর্ঘমেয়াদী বিনিয়োগ ও সঞ্চয়ের ফল বাস্তবে দেখা যেতে শুরু করে।"
        ),
    },
    {
        "range": (43, 48),
        "planet": "কেতু",
        "planet_en": "Ketu",
        "life_progression": (
            "সক্রিয় দায়িত্ব থেকে ধীরে ধীরে অবসরের দিকে।"
        ),
        "father_income_focus": (
            "ঋণমুক্ত আর্থিক অবস্থান সুরক্ষিত করার সময়।"
        ),
    },
    {
        "range": (49, 54),
        "planet": "শুক্র",
        "planet_en": "Venus",
        "life_progression": (
            "স্বস্তিদায়ক গৃহজীবন ও সম্পদ একত্রীকরণের পর্যায়।"
        ),
        "father_income_focus": (
            "অর্জিত সম্পদ সংহত করা ও পারিবারিক স্থিতিশীলতা বজায় রাখা।"
        ),
    },
    {
        "range": (55, 60),
        "planet": "সূর্য (সমাপ্তি)",
        "planet_en": "Sun / Completion",
        "life_progression": (
            "৬০ বছরের ষষ্টিপূর্তি চক্রের সমাপ্তি — বহু-প্রজন্মভিত্তিক পারিবারিক "
            "ব্যবস্থার স্থিতিশীলতা।"
        ),
        "father_income_focus": (
            "সম্পদ হস্তান্তর ও পরবর্তী প্রজন্মের জন্য উত্তরাধিকার প্রস্তুতি।"
        ),
    },
]


def get_phase_for_age(age: int):
    if age < 1:
        age = 1
    for phase in LIFE_PHASES:
        start, end = phase["range"]
        if start <= age <= end:
            return phase
    return LIFE_PHASES[-1]


def calculate_age(dob: date, on_date: date = None) -> int:
    on_date = on_date or date.today()
    years = on_date.year - dob.year
    if (on_date.month, on_date.day) < (dob.month, dob.day):
        years -= 1
    return max(years, 0)


def is_financial_dependent_phase(age: int) -> bool:
    return age <= 18


def generate_life_financial_steps(name, dob, chart=None):
    age = calculate_age(dob)
    phase = get_phase_for_age(age)
    dependent = is_financial_dependent_phase(age)

    steps = []

    steps.append({
        "title": "ধাপ ১ — বর্তমান জীবনচক্র পর্যায়",
        "content": (
            f"**{name}** — বর্তমান বয়স **{age} বছর**।\n\n"
            f"এই বয়স পড়ছে **{phase['range'][0]}–{phase['range'][1]} বছর** "
            f"পর্যায়ে, যার শাসক গ্রহ **{phase['planet']} ({phase['planet_en']})**।"
        ),
    })

    steps.append({
        "title": "ধাপ ২ — জীবন ও জ্যোতিষ অগ্রগতি (Life & Astrological Progression)",
        "content": phase["life_progression"],
    })

    steps.append({
        "title": "ধাপ ৩ — পারিবারিক অর্থনীতি ও বাবার আয়ের যোগসূত্র",
        "content": (
            phase["father_income_focus"]
            + ("\n\n📌 এই পর্যায়ে (১৮ বছর বা তার কম) বাবার আয়, কর্মজীবনের "
               "স্থিরতা ও পারিবারিক অর্থনৈতিক বৃদ্ধির উপর ৫০% ফোকাস প্রযোজ্য।"
               if dependent else
               "\n\n📌 এই পর্যায়ে ফোকাস ধীরে ধীরে বাবার সরাসরি আয় থেকে "
               "উচ্চশিক্ষা তহবিল, যৌথ পারিবারিক সম্পদ ও ব্যক্তিগত ক্যারিয়ার "
               "প্রতিষ্ঠার দিকে সরে যায়।")
        ),
    })

    if chart and chart.get("current_dasha"):
        steps.append({
            "title": "ধাপ ৪ — বর্তমান গ্রহদশার সাথে মিল",
            "content": (
                f"বর্তমানে **{chart['current_dasha']['lord']} মহাদশা** চলছে। "
                f"এটি এই জীবনচক্র পর্যায়ের ({phase['planet']}) সাথে মিলিয়ে "
                f"বাস্তব পরিস্থিতি যাচাই করা যেতে পারে।"
            ),
        })

    return steps
  
