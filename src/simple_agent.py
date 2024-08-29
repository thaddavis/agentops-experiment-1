from openai import OpenAI
import agentops
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "<your_openai_key>"
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY") or "<your_agentops_key>"

print('Hello World!')

openai = OpenAI(api_key=OPENAI_API_KEY)
agentops.init(AGENTOPS_API_KEY, default_tags=["openai-gpt-notebook"])

message = [{"role": "user", "content": "Write a 12 word poem about secret agents."}]
response = openai.chat.completions.create(
    model="gpt-3.5-turbo", messages=message, temperature=0.5, stream=False
)
print(response.choices[0].message.content)

agentops.end_session("Success")
