from .models import UserProfile
import os
import io
import json
from google.cloud import vision
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from django.conf import settings
from datetime import date

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "default-secret-key")

def process_resume_and_update_profile(profile: UserProfile, resume_path: str):
    client = vision.ImageAnnotatorClient.from_service_account_file("boreal-logic-460821-j6-b607b01a3bdb.json")
    with io.open(resume_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    detected_text = texts[0].description if texts else ""

    llm = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)
    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the following fields from the user's text: interests, hobbies, and background. Return them in JSON format."),
        ("user", "{raw_text}")
    ])
    extract_chain = extract_prompt | llm
    structured_response = extract_chain.invoke({"raw_text": detected_text})

    try:
        user_data = json.loads(structured_response.content)
    except Exception:
        user_data = {}

    profile.interests = user_data.get("interests", "")
    profile.hobbies = user_data.get("hobbies", "")
    profile.bio = user_data.get("background", "")
    profile.save()

def generate_recommendations(bio, interests, competitions):
    competitions_list = [
        {
            "title": c.title,
            "date": str(c.date),
            "direction": c.direction,
            "description": c.description,
            "tags": c.tags,
        }
        for c in competitions
    ]
    prompt = (
        "У пользователя следующая информация:\n"
        f"Биография: {bio}\n"
        f"Интересы: {interests}\n\n"
        "Вот список конкурсов:\n"
        f"{competitions_list}\n\n"
        "Выбери и перечисли наиболее подходящие конкурсы для пользователя (только названия), основываясь на его интересах и биографии. Ответ верни в виде списка."
    )

    llm = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)
    print(OPENAI_API_KEY)
    response = llm.invoke(prompt)
    return response.content

def select_best_teammates(current_profile, all_profiles):
    profiles_data = [
        {
            "username": p.user.username,
            "bio": p.bio,
            "interests": p.interests,
            "hobbies": p.hobbies,
        }
        for p in all_profiles if p.user != current_profile.user
    ]
    prompt = (
        f"Профиль пользователя:\n"
        f"Биография: {current_profile.bio}\n"
        f"Интересы: {current_profile.interests}\n"
        f"Хобби: {current_profile.hobbies}\n\n"
        f"Вот профили других пользователей:\n"
        f"{profiles_data}\n\n"
        "Выбери трёх лучших сокомандников для пользователя на основе совпадения интересов, биографии и хобби. "
        "Верни только их username в виде списка Python."
    )

    llm = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)
    response = llm.invoke(prompt)
    try:
        teammates = eval(response.content)
        if isinstance(teammates, list):
            return teammates
    except Exception:
        pass
    return []

def generate_competitions_ai(bio, interests, hobbies):
    today = date.today().strftime("%Y-%m-%d")
    prompt = (
        f"Сегодняшняя дата: {today}\n"
        f"Пользователь:\n"
        f"Биография: {bio}\n"
        f"Интересы: {interests}\n\n"
        f"Хобби: {hobbies}\n\n"
        "Найди 5 конкурсов, которые могли бы заинтересовать этого пользователя."
        "Для каждого конкурса укажи: title (название), date (дата в формате ГГГГ-ММ-ДД), "
        "direction (направление: IT или Hardware), description (короткое описание), tags (через запятую). "
        "Верни результат в формате JSON-списка."
    )
    llm = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)
    response = llm.invoke(prompt)
    try:
        competitions = json.loads(response.content[7:-3])
    except Exception:
        competitions = []
    return competitions