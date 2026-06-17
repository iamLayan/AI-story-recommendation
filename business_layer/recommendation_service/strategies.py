import os
# 🧠 يحتوي على الاستراتيجيات المختلفة لتوليد القصص
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class BaseStoryStrategy:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"  
        )
    print(os.getenv("GROQ_API_KEY"))

    def generate(self, prompt):
        raise NotImplementedError("Subclasses must implement this method")


class CreativeStoryStrategy(BaseStoryStrategy):
    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a creative Arabic storyteller."},
                {"role": "user", "content": f"اكتب قصة إبداعية عن: {prompt}"}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content


class MoralStoryStrategy(BaseStoryStrategy):
    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an Arabic storyteller who writes moral stories with lessons."},
                {"role": "user", "content": f"اكتب قصة تعليمية فيها عبرة عن: {prompt}"}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content


class HorrorStoryStrategy(BaseStoryStrategy):
    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an Arabic horror storyteller."},
                {"role": "user", "content": f"اكتب قصة مرعبة عن: {prompt}"}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content
