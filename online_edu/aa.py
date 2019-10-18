from redisearch import Client,TextField
# 创建一个客户端与给定索引名称
client=Client('myindex',host='101.37.25.38',port='6666')

# 创建索引定义和模式
# client.create_index((TextField('title'),TextField('body')))
print('-------------------')

# 索引文件
# client.add_document('doc2',title='你好',body='中国上下5000年,唐诗三百首',language='chinese')
# 查找搜索
res=client.search(('上下'))

print(res.docs[0].title)
# 创建一个客户端与给定索引名称
# client = Client('myIndex',host='101.37.25.38',port='6666')
#
#
# #创建索引定义和模式
# # client.create_index((TextField('title'), TextField('body')))
#
# #索引文件
# # client.add_document('doc2', title = '你好', body = '我在学习人工智能',language='chinese')
#
# # 查找搜索
# res = client.search("学习")
#
# print(res.docs[0].title)