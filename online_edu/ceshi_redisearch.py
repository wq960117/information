from redisearch import Client, TextField
# 创建一个客户端与给定索引名称
client = Client('AtIndex',host='120.27.246.172',port='6666')


#创建索引定义和模式
client.create_index((TextField('title'), TextField('body')))

#索引文
client.add_document('doc3', title = '你好啊', body = '我在学习人工智能',language='chinese')

# 查找搜索
res = client.search("人工智能")

print(res.docs[0].title)
