from openai import OpenAI
import requests
import pandas as pd
import time

# OpenAI API 설정
client = OpenAI(
    api_key = "(내 openAI api key)"
)

# 네이버 도서 API 설정
NAVER_CLIENT_ID = "(내 Naver api key)"
NAVER_CLIENT_SECRET = "(내 Naver api client secret)"

# Google Books API 설정
GOOGLE_BOOKS_API_KEY = "(내 GoogleBooks api key)"

# 질문 데이터 로드
questions_df = pd.read_csv("generated_book_queries_9.csv")  # 이전에 생성한 질문 데이터 로드
questions = questions_df['question'].tolist()

# 결과 저장용 리스트
results = []

# OpenAI API를 통해 질문에 대한 답변 생성
def generate_answer(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that recommends books based on a given query. Respond with only the book title. Do not include any author names, additional information, or formatting such as quotation marks, parentheses, or numbering."},
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"OpenAI API 호출 오류: {e}")
        return None

# 네이버 도서 API로 도서 검증
def verify_with_naver(book_title):
    url = "https://openapi.naver.com/v1/search/book.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {"query": book_title, "display": 1}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json().get('items', [])
        return len(items) > 0
    return False

# Google Books API로 도서 검증
def verify_with_google(book_title):
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}&key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get('items', [])
        return len(items) > 0
    return False

# 도서 검증 (네이버와 Google Books 교차 검증)
def verify_book(book_title):
    if not book_title:
        return False
    naver_verified = verify_with_naver(book_title)
    google_verified = verify_with_google(book_title)
    return naver_verified or google_verified

# 질문 데이터를 순회하며 답변 생성 및 검증
for question in questions:
    print(f"질문: {question}")
    answer = generate_answer(question)
    if answer:
        print(f"생성된 답변: {answer}")
        if verify_book(answer):
            print("검증 성공: 실존 도서입니다.")
            results.append({"question": question, "answer": answer})
        else:
            print("검증 실패: 실존 도서가 아닙니다.")
            results.append({"question": question, "answer": ""})
    else:
        print("답변 생성 실패.")
        results.append({"question": question, "answer": ""})
    time.sleep(1)  # API 호출 제한을 고려해 딜레이 추가

# 결과를 데이터프레임으로 저장
results_df = pd.DataFrame(results)
results_df.to_csv("verified_book_recommendations.csv", index=False, encoding="utf-8-sig")

print("프로세스 완료. 결과는 'verified_book_recommendations.csv' 파일에 저장되었습니다.")
