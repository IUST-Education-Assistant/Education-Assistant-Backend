from langchain_groq import ChatGroq

from core.runtime_config import load_runtime_config

config = load_runtime_config()
llm_model = config.get("GROQ_LLM_MODEL")
api_key = config.get("GROQ_API_KEY")
if not llm_model or not api_key:
    raise RuntimeError(
        "GROQ_LLM_MODEL and GROQ_API_KEY must be set (env vars recommended)"
    )

llm = ChatGroq(model=llm_model, api_key=api_key)


def generate_title(message: list[dict]) -> str:
    prompt = f"""
بر اساس این پیام کاربر یک عنوان مناسب  و کوتاه برای چت ایجاد بکن.
در خروجی فقط عنوان را برگردان.
خروجی تو به همان زبان ورودی کاربر باشد.
پیام کاربر: {message}
    """
    response = llm.invoke(prompt)
    return response.content
