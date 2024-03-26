import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_prompt(colors):
    """
    Creates a prompt for OpenAI API using the extracted colors.
    """
    prompt_lines = ["Мне нужна помощь в определении идеальной цветовой палитры, которая подчеркнет мой цвет кожи и общий цветовой тип. Можете ли вы определить мой цветотип по системе анализа на 12 сезонов (Теплая Весна, Яркая Весна, Светлая Весна, Холодная Весна, Мягкое Лето, Светлое Лето, Холодное Лето, Мягкая Осень, Теплая Осень, Глубокая Осень, Глубокая Зима, Холодная Зима, Яркая Зима)?",
                    "Пожалуйста, начните ваш ответ, указав цветотип, который, по вашему мнению, мне наиболее подходит. Стремитесь к краткости, ответ не должен превышать 456 символов.",
                    "Этот промпт сосредотачивает внимание на главном запросе и стимулирует дать прямой и краткий ответ. Также он уточняет, что детали, предоставленные ниже, это коды цветов, соответствующие физическим особенностям пользователя, что является критически важной информацией для определения цветотипа.",
                    "Ниже представлены коды цветов, относящиеся к моей коже, глазам и волосам:"]
    for feature, codes in colors.items():
        for code in codes:
            prompt_lines.append(f"{feature} — {code}")
    return "\n".join(prompt_lines)


def query_openai(prompt):
    """
    Sends a prompt to the OpenAI API and returns the response.
    """
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.2,
        max_tokens=456,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print(response)
    return response.choices[0].text.strip()
