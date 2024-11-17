import asyncio
import websockets
import pandas as pd
import torch
from utils.Preprocess import Preprocess
from utils.FindAnswer import FindAnswer
from train_tools.qna.create_embedding_data import create_embedding_data

# 전처리 객체 생성
try:
    p = Preprocess(word2index_dic='./train_tools/dict/chatbot_dict.bin',
                   userdic='./utils/user_dic.tsv')
    print("텍스트 전처리기 로드 완료..")
except: print("텍스트 전처리기 로드 실패..")

#엑셀 파일 로드
try:
    df = pd.read_csv('train_tools/qna/question_with_labels_100.csv')
    print("엑셀 파일 로드 완료..")
except: print("엑셀 파일 로드 실패..")

# pt 파일 갱신 및 불러오기
try:
    create_embedding_data = create_embedding_data(df=df, preprocess=p)
    create_embedding_data.create_pt_file()
    embedding_data = torch.load('train_tools/qna/embedding_data.pt')
    print("임베딩 pt 파일 갱신 및 로드 완료..")
except: print("임베딩 pt 파일 갱신 및 로드 실패..")


async def handler(websocket, path):
    async for message in websocket:
        ### message의 score 구해야 함. "안녕하세요", "~~~ 책 추천해줘" 와 같은 말과 유사도 비교하여 0.6 이하라면 "죄송합니다. 아직 준비되지 않은 답변입니다." 출력
        f = FindAnswer(message)
        selected_qes, score, answer, query_intent = f.search(message)
        if score < 0.6: 
            response = "죄송합니다. 아직 준비되지 않은 답변입니다."
        else:
            print(selected_qes) ## 결과 출력 시 출력이 어떤 데이터에 기초했는지 확인하는 용도
            print(query_intent)
            response = answer

        await websocket.send(response)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("서버가 ws://localhost:8765 에서 시작되었습니다.")
        await asyncio.Future()  # 서버가 계속 실행되도록 유지

asyncio.run(main())

