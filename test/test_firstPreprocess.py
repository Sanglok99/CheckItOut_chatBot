from utils.firstPreprocess import Preprocess

sent = "컴공 과사 번호를 알려줘?...!"

p = Preprocess(userdic='../utils/user_dic.tsv')

pos = p.pos(sent)

ret = p.get_keywords(pos, without_tag=False)
print(ret)

ret = p.get_keywords(pos, without_tag=True)
print(ret)