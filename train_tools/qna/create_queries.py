from openai import OpenAI
import pandas as pd
import time

client = OpenAI(api_key="(내 openAI api key)")

# 질문 생성용 프롬프트
generation_prompt = """
여러 주제에 대한 책을 추천받고자 합니다. 1000개의 질문을 만들어 주세요.
각 질문은 한국어로 작성되며, 각각의 주제에 대한 책 추천을 요청하는 형식으로 작성하세요.
예: '한국 역사에 관한 책 추천해줘', '인공지능에 대한 책 뭐가 좋아?', '독일 철학에 대한 책 뭐가 좋을까?', '환경 보호에 관한 책 추천해줄래?', '도시 계획에 관한 책 뭐가 좋아?'
답변은 텍스트로만 구성하고, numbering이나 index는 달지 마세요.
"""

# 질문 데이터 저장
questions = []

# OpenAI API 호출하여 질문 생성
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that generates content in Korean. When asked to generate queries, respond with only the generated queries in Korean, without any additional information, explanations, or numbering."},
        {"role": "user", "content": generation_prompt}
    ],
    max_tokens=2048,  # 한 번에 최대 2048 토큰 사용
    temperature=0.5
)

# 생성된 질문 추출 및 정리
generated_text = response.choices[0].message.content.strip()
questions = [q.strip() for q in generated_text.split("\n") if q.strip()]

# 질문 개수 확인
print(f"생성된 질문 개수: {len(questions)}")

# 질문이 400개가 되지 않으면 추가 요청
while len(questions) < 1000:
    remaining = 1000 - len(questions)
    print(f"{remaining}개의 질문이 더 필요합니다. 추가 생성 요청 중...")

    additional_prompt = f"""
    여러 주제에 대한 책을 추천받고자 합니다. 총 1000개의 질문을 만드는 것을 목표로 하고 있습니다.
    각 질문은 한국어로 작성되며, 각각의 주제에 대한 책 추천을 요청하는 형식으로 작성하세요.
    예: '한국 역사에 관한 책 추천해줘', '인공지능에 대한 책 뭐가 좋아?', '독일 철학에 대한 책 뭐가 좋을까?', '환경 보호에 관한 책 추천해줄래?', '도시 계획에 관한 책 뭐가 좋아?'
    답변은 텍스트로만 구성하고, numbering이나 index는 달지 마세요.
    
    추가로 {remaining}개의 책 추천 질문을 만들어 주세요. 한국어로 작성해 주세요.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates content in Korean. When asked to generate queries, respond with only the generated queries in Korean, without any additional information, explanations, or numbering."},
            {"role": "user", "content": additional_prompt}
        ],
        max_tokens=2048,
        temperature=0.5
    )
    
    # 추가 질문 추출 및 정리
    additional_questions = [q.strip() for q in response.choices[0].message.content.strip().split("\n") if q.strip()]
    questions.extend(additional_questions)
    print(f"생성된 질문 개수: {len(questions)}")

# 중복 제거
questions = list(set(questions))

# 질문을 CSV 파일로 저장
df = pd.DataFrame({"question": questions})
df.to_csv("generated_book_queries_9.csv", index=False, encoding="utf-8-sig")

print("1000개의 질문이 성공적으로 생성되었으며, 'generated_book_queries_9.csv' 파일에 저장되었습니다.")