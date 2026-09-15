from openai import OpenAI

def get_ai_reply(api_key, user_prompt, context):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    system_prompt = f"""
    তুমি একজন অভিজ্ঞ বৈদিক জ্যোতিষী।
    নাম: {context.get('name')}
    নক্ষত্র: {context.get('nakshatra_bn')}
    রাশি: {context.get('rashi_bn')}
    লগ্ন: {context.get('lagna_bn')}
    জন্মস্থান: {context.get('place')}
    বাংলা ভাষায় সংক্ষিপ্ত ও প্রাসঙ্গিক উত্তর দাও।
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
    )

    return response.choices[0].message.content
