import requests
import json
from typing import Dict, NoReturn, TextIO


class LagoInfo(object):
    """
    获取lago网指定关键词数据类

    属性:
        headers: 网页请求头
    """
    def __init__(self) -> NoReturn:
        self.headers = {
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=py',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }

    def get_cookie(self) -> str:
        """
        获取首页Cookies
        :return: 返回Cookie字符串
        """
        # 首页请求
        res = requests.get("https://www.lagou.com", headers=self.headers)
        cookie = dict(res.cookies)['JSESSIONID']
        return cookie

    def get_data_json(self, page: int, kw: str, cookie: str) -> Dict:
        """
        获取数据方法: 从指定url中通过requests请求携带请求头和请求体获取网页中的信息
        :param page: 页数
        :param kw: 关键词
        :param cookie: 首页cookie
        :return: 返回数据字典
        """
        # 请求参数
        params_data = {
            'first': 'true',
            'pn': page,
            'kd': kw
        }
        # 头部添加cookie
        headers = self.headers
        headers['Cookie'] = cookie
        # 发起请求,得到响应数据
        res = requests.post("https://www.lagou.com/jobs/v2/positionAjax.json?needAddtionalResult=false", data=params_data, headers=headers).json()
        return res

    def save_in_json(self, file: TextIO, results: Dict) -> NoReturn:
        """
        保存json文件
        :param file: 目标文件对象
        :param results: 需要保存的数据
        :return: None
        """
        # 获取全局已保存数量
        global result_count
        # 获取结果列表
        res_list = results['content']['positionResult']['result']
        for info in res_list:
            # 合并公司Logo字段
            info['companyLogoFull'] = 'https://www.lgstatic.com/thumbnail_120x120/' + info['companyLogo']
            # 一次向目标文件写入一条数据
            file.writelines(json.dumps(info, ensure_ascii=False) + "\n")
            # 已保存数量自增1
            result_count += 1
            print(f'已保存{result_count}条数据!')


def main(target_file_path: str) -> NoReturn:
    """
    程序主函数
    :param target_file_path: 存储文件路径
    :return: None
    """
    # 实例化LagoInfo类
    lago = LagoInfo()
    # 初始化cookie
    cookie = ""
    # 初始化页码数量
    page_count = 0
    # 因为关键词最多返回30页, 所以下面迭代30次
    for i in range(1, 31):
        # 每十个请求重新获取cookie
        if (i % 10 == 0):
            # 重置cookie
            cookie = lago.get_cookie()
        # 获取数据
        results = lago.get_data_json(2, '大数据', cookie)
        with open(target_file_path, 'a', encoding='utf8') as file:
            # 保存数据
            lago.save_in_json(file, results)
        # 页码数量自增1
        page_count += 1
        print(f'第{page_count}页数据采集完成!')


if __name__ == '__main__':
    # 保存数据文件路径
    target_file_path = r'results.json'
    # 初始化已保存数量
    result_count = 0
    for _ in range(1, 11):
        # 执行主函数
        main(target_file_path)
