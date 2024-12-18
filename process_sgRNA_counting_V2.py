import re
import csv
import argparse
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from os.path import join, exists
from os import makedirs

# 定义一个函数来计算两个序列之间的错配数量
def count_mismatches(seq1, seq2):
    return sum(1 for a, b in zip(seq1, seq2) if a != b)

# 定义一个函数来处理每条read，寻找特定序列后的特征序列，并与参考序列匹配
def process_read(read_data, target_sequence, sequence_length, mismatches_allowed, reference_sequences, barcode_map):
    identifier_line, sequence_line = read_data
    if target_sequence in sequence_line:
        umi_match = re.search(r'UR:Z:(\w+)', identifier_line)
        cell_barcode_match = re.search(r'CB:Z:(\w+)', identifier_line)
        umi = umi_match.group(1) if umi_match else None
        cell_barcode = cell_barcode_match.group(1) if cell_barcode_match else None
        if cell_barcode in barcode_map:
            cell_barcode = barcode_map[cell_barcode]  # 使用合并后的barcode
        start_index = sequence_line.find(target_sequence) + len(target_sequence)
        feature_sequence = sequence_line[start_index:start_index+sequence_length]
        for ref_name, ref_seq in reference_sequences.items():
            if count_mismatches(feature_sequence, ref_seq) <= mismatches_allowed:
                return cell_barcode, feature_sequence, umi, ref_name
    return None

# 设置命令行参数解析器
parser = argparse.ArgumentParser(description='处理FASTQ文件，根据特定序列后的特征序列计算表达量。')
parser.add_argument('-f', '--fastq_file', required=True, help='FASTQ文件的路径。')
parser.add_argument('-r', '--reference_csv', required=True, help='参考序列CSV文件的路径。')
parser.add_argument('-t', '--target_sequence', required=True, help='要搜索的目标序列。')
parser.add_argument('-l', '--sequence_length', type=int, required=True, help='目标序列后要匹配的序列长度。')
parser.add_argument('-n', '--num_threads', type=int, default=4, help='使用的线程数（默认为4）。')
parser.add_argument('-o', '--output_path', required=True, help='结果输出路径。')
parser.add_argument('-m', '--mismatches_allowed', type=int, default=1, help='允许的错配数量（默认为1）。')
parser.add_argument('-c', '--chunk_size', type=int, default=1000000, help='每次处理的reads数量（默认为1000000）。')
parser.add_argument('-b', '--barcode_map_csv', required=True, help='barcode合并关系CSV文件的路径。')

# 解析命令行参数
args = parser.parse_args()

# 读取参考序列
reference_sequences = {}
with open(args.reference_csv, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 跳过标题行
    for row in reader:
        ref_name, ref_seq = row
        reference_sequences[ref_name] = ref_seq

# 读取barcode合并关系
barcode_map = {}
with open(args.barcode_map_csv, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        original_barcode, merged_barcode = row
        barcode_map[original_barcode] = merged_barcode

# 检查输出目录是否存在，如果不存在则创建
if not exists(args.output_path):
    makedirs(args.output_path)

# 初始化结果文件
results_file = join(args.output_path, 'results.csv')
with open(results_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Cell Barcode', 'Feature Sequence', 'UMI', 'Reference Sequence Name'])  # 写入标题行

# 处理reads
def process_chunk(chunk):
    with ThreadPoolExecutor(max_workers=args.num_threads) as executor:
        futures = [executor.submit(process_read, (identifier_line.strip(), sequence_line.strip()), 
                                   args.target_sequence, args.sequence_length, args.mismatches_allowed, reference_sequences, barcode_map) for identifier_line, sequence_line in chunk]
        results = [future.result() for future in futures if future.result()]
    return results

with opCR_1_5_sgRNA_matrix \
    chunk = []
    for i, line in enumerate(file):
        if i % 4 == 0:
            identifier_line = line
        elif i % 4 == 1:
            sequence_line = line
        elif i % 4 == 3:
            chunk.append((identifier_line, sequence_line))
            if len(chunk) >= args.chunk_size:
                results = process_chunk(chunk)
                with open(results_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for result in results:
                        writer.writerow(result)
                chunk = []
    # 处理最后一个chunk
    if chunk:
        results = process_chunk(chunk)
        with open(results_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for result in results:
                writer.writerow(result)

# 对每个细胞条形码和特征序列计数UMI
umi_counts = defaultdict(lambda: {'umis': set(), 'ref_name': None})
with open(results_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 跳过标题行
    for row in reader:
        cell_barcode, feature_sequence, umi, ref_name = row
        umi_counts[(cell_barcode, feature_sequence)]['umis'].add(umi)
        umi_counts[(cell_barcode, feature_sequence)]['ref_name'] = ref_name

# 计算表达量
expression_counts = {key: len(value['umis']) for key, value in umi_counts.items()}

# 将表达量统计结果写入expression_counts.csv文件
expression_counts_file = join(args.output_path, 'expression_counts.csv')
with open(expression_counts_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Cell Barcode', 'Feature Sequence', 'Expression Count', 'Reference Sequence Name'])  # 写入标题行
    for (cell_barcode, feature_sequence), count in expression_counts.items():
        ref_name = umi_counts[(cell_barcode, feature_sequence)]['ref_name']
        writer.writerow([cell_barcode, feature_sequence, count, ref_name])

print(f"结果已写入 {results_file}")
print(f"表达量统计已写入 {expression_counts_file}")
