import os

import openai
import json
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from starlette.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("FAQ.json", encoding="utf-8") as f:
    faq_data = json.load(f)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def answer(request: Request, question: str = Form(...)):
    answer = get_answer(question)
    return templates.TemplateResponse(
        "index.html", {"request": request, "question": question, "answer": answer}
    )


def get_answer(question):
    best_match_question = find_best_match(question)
    if best_match_question:
        answer = query_chatgpt(question, best_match_question)
        return answer
    else:
        return "No answer found"


def find_best_match(question):
    best_match_score = 0
    best_match_question = None

    for faq in faq_data:
        score = calculate_similarity(question, faq["Question_short"])
        if score > best_match_score:
            best_match_score = score
            best_match_question = faq["Question_short"]

    for faq in faq_data:
        for alternative in faq["Question_short_alternatives"]:
            score = calculate_similarity(question, alternative)
            if score > best_match_score:
                best_match_score = score
                best_match_question = faq["Question_short"]

    for faq in faq_data:
        for alternative in faq["Question_original_alternatives"]:
            score = calculate_similarity(question, alternative)
            if score > best_match_score:
                best_match_score = score
                best_match_question = faq["Question_short"]

    for faq in faq_data:
        for keyword in faq["Keywords"]:
            score = calculate_similarity(question, keyword)
            if score > best_match_score:
                best_match_score = score
                best_match_question = faq["Question_short"]

    print(best_match_question)
    return best_match_question


def calculate_similarity(question1, question2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([question1, question2])
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity_score


def query_chatgpt(user_question, faq_question):
    faq = next(
        (item for item in faq_data if item["Question_short"] == faq_question), None
    )

    if faq is None:
        return "No answer found"

    note = faq["Notes"]

    messages = [
        {"role": "system", "content": note},
        {"role": "user", "content": f"User: {user_question}"},
        {"role": "assistant", "content": faq_question},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=3500,
        temperature=0.7,
    )

    if response.choices and response.choices[0].message["role"] == "assistant":
        return response.choices[0].message["content"].strip()
    else:
        return "No answer found"
