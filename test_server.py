# 클라이언트 연결 없이 챗봇 작동 확인하는 테스트 파일

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

def main():
    while True:
        # 사용자 입력 받기
        test_message = input("\n챗봇에게 질문을 입력하세요 (종료하려면 'exit' 입력): ").strip()
        if test_message.lower() == 'exit':
            print("챗봇 테스트를 종료합니다.")
            break

        # 입력 문자열 정리
        try:
            message = message.encode("utf-8").decode("utf-8")  # UTF-8로 변환 가능한지 확인
        except UnicodeEncodeError as e:
            print(f"입력 문자열에 유효하지 않은 문자가 포함되어 있습니다: {e}")
            continue

        f = FindAnswer(df=df, embedding_data=embedding_data ,preprocess=p)
        selected_qes, score, answer = f.search(test_message)

        if score < 0.6: 
                response = "죄송합니다. 아직 준비되지 않은 답변입니다."
        else:
            print(f"관련 질문: {selected_qes}")  # 디버깅 및 확인용(출력이 어떤 데이터에 기초했는지 확인)
            response = answer

        print(f"챗봇 응답: {response}")

if __name__ == '__main__':
    main()
