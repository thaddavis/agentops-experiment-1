import agentops
from agentops import track_agent
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from IPython.display import display, Markdown

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "<your_openai_key>"
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY") or "<your_agentops_key>"
logging.basicConfig(
    level=logging.DEBUG
)  # this will let us see that calls are assigned to an agent

agentops.init(AGENTOPS_API_KEY, default_tags=["multi-agent-notebook"])
openai_client = OpenAI(api_key=OPENAI_API_KEY)

@track_agent(name="qa")
class QaAgent:
    def completion(self, prompt: str):
        res = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a qa engineer and only output python code, no markdown tags.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        return res.choices[0].message.content

@track_agent(name="engineer")
class EngineerAgent:
    def completion(self, prompt: str):
        res = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a software engineer and only output python code, no markdown tags.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        return res.choices[0].message.content
    
qa = QaAgent()
engineer = EngineerAgent()

generated_func = engineer.completion("python function to test prime number")

display(Markdown("```python\n" + generated_func + "\n```"))

generated_test = qa.completion(
    "Write a python unit test that tests the following function: \n " + generated_func
)

display(Markdown("```python\n" + generated_test + "\n```"))

res = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are not a tracked agent"},
        {"role": "user", "content": "Say hello"},
    ],
)
res.choices[0].message.content

agentops.end_session("Success")