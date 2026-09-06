import os
from getpass import getpass

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

GROQ_API_KEY =getpass("Enter you Groq API key: ")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

print()
chat_history= []

while True:
    prompt = input("User: ")
    chat_history.append(HumanMessage(prompt))
    client = ChatGroq(model="openai/gpt-oss-120b")
    response = client.invoke(chat_history)
    chat_history.append(response)

    print("AI:", response.content)