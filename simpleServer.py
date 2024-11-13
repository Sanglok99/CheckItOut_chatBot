import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        if message == "안녕하세요.":
            response = "반갑습니다."
        elif message == "조선과 고려에 대한 책 추천해줘.":
            response = "조선왕조실록"
        else:
            response = "죄송합니다. 아직 준비되지 않은 답변입니다."
        await websocket.send(response)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("서버가 ws://localhost:8765 에서 시작되었습니다.")
        await asyncio.Future()  # 서버가 계속 실행되도록 유지

asyncio.run(main())