from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

groq_client  = Groq(api_key=(os.getenv("GROQ_API_KEY")))

def hint(problem_description, user_code):
    messages = [
        {
        "role":"system",
        "content": "You are a DSA expert. Give hints only, never full solutions"
    },
    {
        "role": "user",
        "content": f"Problem: {problem_description}\nMy code so far: {user_code}\nGive me a hint."
    }
    ]
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = messages
    )
    reply = response.choices[0].message.content

    return reply