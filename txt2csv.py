import csv

# 设置输入TXT文件和输出CSV文件的路径
input_txt_path = 'TD_barcodeTranslate.txt'
output_csv_path = 'TD_barcodeTranslate.csv'

# 打开TXT文件和CSV文件
with open(input_txt_path, 'r') as txtfile, open(output_csv_path, 'w', newline='') as csvfile:
    # 创建CSV写入器
    writer = csv.writer(csvfile)

    # 逐行读取TXT文件
    for line in txtfile:
        # 去除行尾的换行符并按制表符分割
        row = line.strip().split('\t')
        # 将分割后的行写入CSV文件
        writer.writerow(row)

print(f"TXT文件已转换为CSV文件：{output_csv_path}")
