!pip install python-dotenv
!pip install openai
!pip install anthropic

import os 
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from IPython.display import Markdown, display, update_display

load_dotenv(override=True)
os.environ["OPENAI_API_KEY"] = "KEY"
os.environ["ANTHROPIC_KEY"] = "KEY"

openai_api_key = os.getenv("OPENAI_API_KEY")
claude = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_KEY")
)


if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if claude:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

openai = OpenAI()
calude = anthropic.Anthropic()

system_message = "You are an assistant that is great at telling jokes"
user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"
prompts = [{"role":"system", "content":system_message}, {"role":"user", "content":user_prompt}]

completion = openai.chat.completions.create(
    model='gpt-4o',
    messages=prompts,
    temperature=0.4
)
print(completion.choices[0].message.content)

message = claude.messages.create(
    model="claude-3-7-sonnet-latest",
    max_tokens=200,
    temperature=0.7,
    system=system_message,
    messages=[
        {"role": "user", "content": user_prompt},
    ],
)

print(message.content[0].text)


#Conversation
gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"

gpt_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."
claude_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

gpt_messages = ["Hi there"]
claude_messages = ["Hi"]

def call_gpt():
  messages = [{"role":"system","content":gpt_system}]
  for gpt,claude in zip(gpt_messages,claude_messages):
    messages.append({"role": "assistant", "content": gpt})
    messages.append({"role": "assistant", "content": claude})
  completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
  return completion.choices[0].message.content

def call_claude():
    messages = []
    for gpt, claude_message in zip(gpt_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    message = claude.messages.create(
        model=claude_model,
        system=claude_system,
        messages=messages,
        max_tokens=500
    )
    return message.content[0].text


gpt_messages = ["Hi there"]
claude_messages = ["Hi"]

print(f"GPT:\n{gpt_messages[0]}\n")
print(f"Claude:\n{claude_messages[0]}\n")

for i in range(5):
  gpt_next = call_gpt()
  print(f"GPT:\n{gpt_next}\n")
  gpt_messages.append(gpt_next)

  claude_next = call_claude()
  print(f"Claude:\n{claude_next}\n")
  claude_messages.append(claude_next)
