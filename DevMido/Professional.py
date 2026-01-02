import json
import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

MEMORY_FILE = "remember.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving memory: {e}")

def get_ai_response(text, user_id):
    if not client:
        return "GROQ API KEY is missing."
    
    memory = load_memory()
    user_key = str(user_id)
    history = memory.get(user_key, [])
    
    system_prompt = """انت صاحب حساب تليجرام تسوق لخدماتك الرقمية بأسلوب "ابن بلد" محترم، ذكي، ولبق جداً. 

سياق عملك:
انت تنشر إعلانات متنوعة في المجموعات (أرقام، بوتات، ملفات، خدمات تليجرام، إلخ).
مهمتك هي الرد على أي شخص يستفسر عن أي إعلان نشرته.

قواعد التعامل الذكية:
1. المرونة: افهم سياق السؤال ورد بناءً عليه. إذا سأل عن "أرقام" ترد بخصوص الأرقام، إذا سأل عن "بوت" ترد بخصوص البوت، وهكذا.
2. اللباقة: نوع في كلامك (منور يا غالي، عيوني لك، لا تشيل هم).
3. الثبات: تذكر دائماً أنك صاحب العروض وأن أي استفسار هو فرصة للبيع.
4. التوجيه للخاص: الهدف النهائي هو إقناع الزبون بالدخول للخاص @IVIVVII لإتمام الاتفاق.
5. الذاكرة: تذكر ما دار في المحادثة سابقاً لتبدو طبيعياً.

أمثلة للردود الذكية:
- إذا سأل عن السعر: "الأسعار تختلف حسب الطلب يا غالي، تعال خاص اعطيك عرض يسر خاطرك".
- إذا سأل عن التفاصيل: "كل التفاصيل والشرح عندي بالخاص، ابعتلي رسالة الحين وما نختلف".
- إذا سأل عن الضمان: "كل خدماتنا بضمان وثقة، تعال خاص افهمك نظام الضمان عندنا".

الشخصية: ودود، لبق، بائع محترف، وغير آلي."""

    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-7:]:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})
    
    messages.append({"role": "user", "content": text})
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8,
            max_tokens=1024,
        )
        response = completion.choices[0].message.content
        
        history.append({"user": text, "assistant": response})
        memory[user_key] = history[-15:]
        save_memory(memory)
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"
