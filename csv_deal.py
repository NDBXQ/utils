import csv

def process_csv(file_path):
    result = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, start=1):
            # print(row)
            # 将每一行数据转换为列表
            row_list = []
            for value in row.values():
                row_list.append(value)
            id_ = row_list[0]
            del row_list[0]
            result[str(id_)] = row_list
    return result

if __name__ == '__main__':
    # 调用函数并传入CSV文件路径
    file_path = '../标签推荐测试数据.csv'
    processed_data = process_csv(file_path)

    print(processed_data)
    # 打印处理后的数据
    # for row in processed_data:
    #     print(row)