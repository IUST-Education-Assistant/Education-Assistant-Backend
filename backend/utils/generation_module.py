from openai import OpenAI
from core.runtime_config import load_runtime_config

config = load_runtime_config()
llm_model = config.get("GROQ_LLM_MODEL")
api_key = config.get("GROQ_API_KEY")
if not llm_model or not api_key:
    raise RuntimeError(
        "GROQ_LLM_MODEL and GROQ_API_KEY must be set (env vars recommended)"
    )


def ask_groq_oss(prompt: str) -> str:
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": """تو یک دستیار مجازی آموزش دانشگاه علم و صنعت هستی. وظیفه‌ی تو این است که به سوالات دانشجویان در مورد قوانین، رویه‌ها و روندهای موجود در آموزش دانشگاه پاسخ بدهی. پاسخ‌ها باید:
1. **دقیق و صحیح** باشند و بر اساس قوانین و فرآیندهای واقعی دانشگاه ارائه شوند.  
2. **شفاف و قابل فهم** برای دانشجویان باشند، طوری که اگر کسی تازه وارد دانشگاه شده هم متوجه شود.  
3. **مختصر و مفید** باشند، ولی در صورت نیاز می‌توانی مثال یا توضیح کوتاه هم بدهی.  
4. اگر سوال خارج از حوزه آموزش دانشگاه بود یا پاسخی ندارد، مودبانه اعلام کن که نمی‌توانی پاسخ دهی.
همیشه هدف این است که دانشجویان بتوانند **به راحتی روندها و قوانین آموزشی را درک کنند و راهنمایی عملی برای امورشان دریافت کنند**.""",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    return response.choices[0].message.content
