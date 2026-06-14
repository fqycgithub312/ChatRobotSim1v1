from openai import OpenAI
from dotenv import load_dotenv
import os
# base_url = "https://api.deepseek.com"
load_dotenv()
base_url = os.getenv("base_url3")
key = os.getenv("key3")
model = "deepseek-v4-flash"

# for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
client = OpenAI(
    api_key=key,
    base_url=base_url
)
messages = [
    {"role": "system", "content": ""},
    {"role": "user", "content": "你是谁"}
]
response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=1000,
    temperature=0.7,
    stop=["============================"],
    stream=True,
)
for chunk in response:
    text = chunk.choices[0].delta.content
    if chunk.choices[0] and (text is not None):
        print(f"{text}", end="", flush=False)
print(f"\n回答完毕！")
