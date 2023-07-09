import re
import json
import pymysql

# 读取JSON
with open('worker.json', 'r') as file:
    pre_worker_data = json.load(file)

# 将JSON转为字符串
worker_data = str(pre_worker_data)

# 正则匹配数据
specified_word1 = "name"
pattern1 = r"\b" + re.escape(specified_word1) + r"\b(.{10})"
matchs1 = re.findall(pattern1, worker_data)

specified_word2 = "minerAccountId"
pattern2 = r"\b" + re.escape(specified_word2) + r"\b(.{53})"
matchs2 = re.findall(pattern2, worker_data)

# 创建字典并处理数据
result_dict = {}
for match_key, match_value in zip(matchs1, (match[0:53] for match in matchs2)):
    result_dict[match_key] = match_value

new_dict = {}
for key, value in result_dict.items():
    new_key = key.replace(" ", "").replace(":", "").replace("'", "")
    new_value = value.replace(" ", "").replace(":", "").replace("'", "")
    new_dict[new_key] = new_value

# 连接到MySQL数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='********',
    database='********'
)
cursor = conn.cursor()

# 创建workers表
create_table_query = "CREATE TABLE workers (name VARCHAR(50), minerAccountId VARCHAR(50), city VARCHAR(50))"
cursor.execute(create_table_query)

# 插入数据到workers表
for name, minerAccountId in new_dict.items():
    insert_query = "INSERT INTO workers (name, minerAccountId, city) VALUES (%s, %s, '南充')"
    values = (name, minerAccountId)
    cursor.execute(insert_query, values)

# 提交事务和关闭连接
conn.commit()
conn.close()

# 打印结果
print(new_dict)
print(f'一共获取到{len(new_dict)}台机器的数据')
