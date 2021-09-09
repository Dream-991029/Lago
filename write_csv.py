import csv
from typing import Dict, Tuple, List, Set, NoReturn, Any


class Csv(object):
    """
    封装csv写入类。

    该类包含列表嵌套字典所涉及到的一些常用属性。

    属性:
        file_path: string类型的目标文件路径
        data_list: list类型的数据
        count: int类型计数器
    """

    def __init__(self) -> NoReturn:
        pass

    def append_csv(self, file_path: str, data_list: List, count: int) -> int:
        """
        创建csv并追加数据
            :param file_path: 目标文件路径
            :param data_list: 数据列表(列表嵌套字典)
            :param count: 计数器
            :return num: 返回最终计数器数量
        """
        with open(file_path, 'a+', encoding='utf8', newline='') as file:
            f_csv = csv.DictWriter(file, data_list[0].keys())
            # 回退指针到首行
            file.seek(0)
            if file.readline().strip("\n") == "":
                f_csv.writeheader()
            f_csv.writerows(data_list)
        num = count + len(data_list)
        print(f"{num}条数据, 写入完成!!!!!")
        return num
