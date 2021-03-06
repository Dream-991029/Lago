from write_csv import Csv
from typing import Any, TextIO, NoReturn
import json


def salary_clean(data: Any) -> str:
    """
    处理薪资函数
    :param data: 需要处理的数据
    :return: 返回处理后的数据
    """
    # 判断处理数据是否为None
    if data is None:
        data = ""
    # 去掉字符串中的k和空格
    data = data.replace('k', '').replace(' ', "")
    print(data)
    return data


def list_clean(data: Any) -> str:
    """
    处理技能、福利、岗位函数
    :param data: 需要处理的数据
    :return: 返回处理后的数据
    """
    # 判断处理数据是否为None
    if data is None:
        data = ""
    # 判断处理数据是否是列表
    elif isinstance(data, list):
        # 空列表
        if len(data) == 0:
            data = ""
        else:
            for i in data:
                if i is None:
                    data = ""
                # 数据中是否有｜
                elif "｜" in i:
                    info = i.split('｜')
                    for k in info:
                        # 将以｜分割的数据追加到数组中
                        data.append(k.strip())
                    # 移除带｜的数据
                    data.remove(i)
            # 将列表中的每个元素以,分割
            data = "-".join(data)
    return data


def main(file: TextIO, target_file_path: str) -> NoReturn:
    """
    程序主函数
    :param file: json文件对象
    :param target_file_path: csv文件路径
    :return: None
    """
    # 初始化列表, 用于存储字典数据
    results = []
    # 迭代json文件对象
    for line_data in file:
        # json字符串转化成字典
        line_data = json.loads(line_data)
        # 创建一个对象, 装处理后的结果
        obj = {}
        # 对字典进行预处理
        for key in line_data:
            if key in ('salary',):
                obj['薪水'] = salary_clean(line_data[key])
            elif key in ('skillLables', 'positionLables', 'companyLabelList'):
                if key in ('skillLables',):
                    obj['技能'] = list_clean(line_data[key])
                elif key in ('positionLables',):
                    obj['岗位'] = list_clean(line_data[key])
                elif key in ('companyLabelList',):
                    obj['福利'] = list_clean(line_data[key])
            elif key in ('city',):
                obj['城市'] = line_data[key].strip()
        # 将处理后的结果装进数组
        results.append(obj)
    # 初始化写入csv类
    csv = Csv()
    # 写入csv
    csv.append_csv(target_file_path, results, 0)


if __name__ == '__main__':
    # json文件路径
    file_path = r'results.json'
    # csv文件路径
    target_file_path = r'results.csv'
    with open(file_path, encoding='utf8') as file:
        main(file, target_file_path)
