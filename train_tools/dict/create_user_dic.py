# user_dic을 생성
# 아직 생성 안함

import csv

# 데이터 정의
data = [
    ["추천", "NNG"],
    ["기초", "NNG"],
    ["다루다", "VV"],
    ["좋다", "VA"],
    ["있다", "VV"]
]

# TSV 파일 생성
with open("user_dic.tsv", mode="w", newline="", encoding="utf-8") as file:
    tsv_writer = csv.writer(file, delimiter="\t")
    tsv_writer.writerows(data)

print("TSV 파일 생성 완료!")
