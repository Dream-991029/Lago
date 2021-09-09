import pandas as pd
import json


with open(r'C:\Users\pc\Desktop\lagou.json', encoding='utf8') as file:
    info_list = json.loads(file.read())
    data = {
        '岗位名称': [val['岗位名称'] for val in info_list],
        '薪资': [val['薪资'] for val in info_list],
        '工作地点': [val['工作地点'] for val in info_list],
        '公司名称': [val['公司名称'] for val in info_list],
        '职位福利': [val['职位福利'] for val in info_list],
        '任职要求': [val['任职要求'] for val in info_list]
    }
    df = pd.DataFrame(data)
    df.to_csv('results2.csv', encoding='gbk', header=True, index=False)
#     info_list = [json.dumps(val, ensure_ascii=False) for val in _list]
#     info_list = sorted(set(info_list), key=info_list.index)
#     print(len(info_list))
#     for info in info_list:
#         print(info)
