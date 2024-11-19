import asyncio
import websockets

# WebSocket 클라이언트 함수
async def test():
    ws_app = await websockets.connect("ws://aws_instance_public_ip:8765", ping_interval=None)
    while True:
        test_message = input("test message 입력(exit 입력 시 종료):")

        if test_message.lower() == "exit":
            print("WebSocket 연결 종료 중...")
            await ws_app.close()
            break
        
        try:
            test_message = test_message.encode("utf-8", errors="replace").decode("utf-8")
            await ws_app.send(test_message)
            response = await ws_app.recv()
            print(f"서버 응답: {response}")
            await asyncio.sleep(1)  # 비동기 대기
        except Exception as e:
            print(f"Failed to connect to WebSocket server: {e}")

# 비동기 루프 시작
if __name__ == "__main__":
    asyncio.run(test())
