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
                   userdic=None)
    print("텍스트 전처리기 로드 완료..")
except: print("텍스트 전처리기 로드 실패..")

#엑셀 파일 로드
try:
    df = pd.read_csv('train_tools/qna/verified_book_recommendations.csv')
    print("엑셀 파일 로드 완료..")
except: print("엑셀 파일 로드 실패..")

# pt 파일 갱신 및 불러오기
try:
    create_embedding_data = create_embedding_data(df=df, preprocess=p)
    create_embedding_data.create_pt_file()
    embedding_data = torch.load('train_tools/qna/embedding_data.pt')
    print("임베딩 pt 파일 갱신 및 로드 완료..")
except: print("임베딩 pt 파일 갱신 및 로드 실패..")


# 텍스트 기반 Ping 메시지 전송
async def send_ping(websocket):
    try:
        while True:
            await websocket.send("Ping")  # 텍스트 기반 ping 전송
            print("Ping 전송")
            await asyncio.sleep(30)  # 30초마다 Ping 전송
    except websockets.ConnectionClosed:
        print("클라이언트와의 연결이 닫혔습니다.")
    except Exception as e:
        print(f"Ping 전송 중 오류 발생: {e}")

async def handler(websocket):
    ping_task = asyncio.create_task(send_ping(websocket))  # Ping 작업 실행
    try:
        async for message in websocket:
            # 'pong' 메시지 필터링
            if message == 'Pong':
                print("Pong 받음")
                continue # 'pong' 메시지는 무시하고 다음 메시지를 기다림

            # 여기서부터는 일반 메시지 처리
            f = FindAnswer(df=df, embedding_data=embedding_data ,preprocess=p)
            selected_qes, score, answer = f.search(message)
            if score < 0.5: ### 유사도 0.5로 수정!!! ###
                response = "죄송합니다. 아직 준비되지 않은 답변입니다."
            else:
                print(selected_qes) ## 결과 출력 시 출력이 어떤 데이터에 기초했는지 확인하는 용도
                response = answer

            await websocket.send(response)
    except websockets.ConnectionClosedError as e:
        print(f"연결 종료: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        ping_task.cancel()  # Ping 태스크 중지
        print("Ping 전송 태스크 중지")
        await websocket.close()
        print("WebSocket 연결이 닫혔습니다.")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("서버가 ws://localhost:8765 에서 시작되었습니다.")
        await asyncio.Future()  # 서버가 계속 실행되도록 유지

asyncio.run(main())