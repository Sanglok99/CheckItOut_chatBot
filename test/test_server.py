import asyncio
import websockets
import pandas as pd
import torch
from utils.Preprocess import Preprocess
from utils.FindAnswer import FindAnswer
from train_tools.qna.create_embedding_data import create_embedding_data

# 전처리 객체 생성
try:
    p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
                   userdic='../utils/user_dic.tsv')
    print("텍스트 전처리기 로드 완료..")
except: print("텍스트 전처리기 로드 실패..")

#엑셀 파일 로드
try:
    df = pd.read_csv('./train_tools/qna/question_with_labels_100.csv')
    print("엑셀 파일 로드 완료..")
except: print("엑셀 파일 로드 실패..")

# pt 파일 갱신 및 불러오기
try:
    create_embedding_data = create_embedding_data(df=df, preprocess=p)
    create_embedding_data.create_pt_file()
    embedding_data = torch.load('./train_tools/qna/embedding_data.pt')
    print("임베딩 pt 파일 갱신 및 로드 완료..")
except: print("임베딩 pt 파일 갱신 및 로드 실패..")
