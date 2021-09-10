import pandas as pd
import json
import re
from typing import Dict, NoReturn


def write_csv(target_file_path: str, results: Dict) -> NoReturn:
    """
    写入csv方法
    :param target_file_path: 写入csv的路径
    :param results: 字典结果
    :return: None
    """
    df = pd.DataFrame(results)
    df.to_csv(target_file_path, encoding='GBK', header=True, index=False)


def clean_salary(res: str) -> Dict:
    """
    清洗薪资方法
    :param res: 需要清洗的数据
    :return: 返回清洗后的数据
    """
    reg = re.compile(r"(.*)k-(.*)k")
    salary_list = [re.search(reg, res).group(1), re.search(reg, res).group(2)]
    results = {
        'min': salary_list[0],
        'max': salary_list[1],
        'ran': '-'.join(salary_list)
    }
    return results


def clean_welfare(res: str) -> str:
    """
    清洗福利数据
    :param res: 需需要清洗的数据
    :return: 返回清洗后的数据
    """
    res = res.replace('"', "").replace('。', '').strip('\n').strip('、')
    if '，' in res:
        res = '-'.join(res.split('，'))
    elif '、' in res:
        res = '-'.join(res.split('、'))
    elif ' ' in res:
        res = '-'.join(res.split(' '))
    elif ',' in res:
        res = '-'.join(res.split(','))
    elif '；' in res:
        res = '-'.join(res.split('；'))
    elif '**' in res:
        res = '-'.join(res.split('**'))
    elif '/' in res:
        res = '-'.join(res.split('/'))
    return res


def main(file_path: str, target_file_path: str) -> NoReturn:
    """
    程序主函数
    :param file_path: json文件路径
    :param target_file_path: csv存储路径
    :return: None
    """
    with open(file_path, encoding='utf8') as file:
        results = {
            '岗位名称': [],
            '薪资范围': [],
            '最低薪资': [],
            '最高薪资': [],
            '工作地点': [],
            '公司名称': [],
            '职位福利': [],
            '任职要求': []
        }
        for info in file:
            obj = json.loads(info)
            salary_dict = clean_salary(obj['salary'])
            results['岗位名称'].append(obj['positionName'].strip())
            results['薪资范围'].append(salary_dict['ran'])
            results['最低薪资'].append(salary_dict['min'])
            results['最高薪资'].append(salary_dict['max'])
            results['工作地点'].append(obj['city'].strip())
            results['公司名称'].append(obj['companyFullName'].strip())
            results['职位福利'].append(clean_welfare(obj['positionAdvantage']))
            results['任职要求'].append(obj['education'].strip())

        write_csv(target_file_path, results)


if __name__ == '__main__':
    file_path = r'results.json'
    target_file_path = r'lago_data.csv'
    main(file_path, target_file_path)
