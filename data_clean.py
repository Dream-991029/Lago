from write_csv import Csv
from typing import Dict, Any, TextIO, NoReturn
import json


def salary_clean(data: Any):
    if data is None:
        data = ""
    res = data.replace('k', '')
    return res


def position_clean(data):
    pass


def skill_clean(data):
    pass


def welfare_clean(data):
    pass


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
            elif key in ('',):
                pass
            elif key in ('',):
                pass
            elif key in ('',):
                pass
            elif key in ('',):
                pass
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
