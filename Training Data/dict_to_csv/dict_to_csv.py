import csv
# 把txt文件中存储的dict转换成csv文件
def dict_to_csv(file_name):
    # 读取txt文件
    with open(file_name, 'r') as f:
        lines = f.readlines()
    # 读取txt文件中的dict
    dicts = [eval(line) for line in lines]
    # 获取dict的key
    keys = dicts[0].keys()
    # 创建csv文件
    with open(file_name.split('.')[0]+'.csv', 'w', newline='') as f:
        # 创建csv文件的写入器
        writer = csv.writer(f)
        # 写入csv文件的第一行
        writer.writerow(keys)
        # 写入csv文件的其余行
        for dict in dicts:
            writer.writerow(dict.values())

if __name__ == '__main__':
    # 把txt文件中存储的dict转换成csv文件
    dict_to_csv('processing_capabilities.txt')
    dict_to_csv('storage_capabilities.txt')
    dict_to_csv('task_storage.txt')
    dict_to_csv('task_processing.txt')
    dict_to_csv('data_volumes.txt')
    dict_to_csv('max_delays.txt')
    
    
    
