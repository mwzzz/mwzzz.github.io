import pandas as pd

# 读取 Excel 文件
file_path = 'E:/新建 XLSX 工作表.xlsx'
df = pd.read_excel(file_path)

# 1. 筛选集客业务级别等于“AAA”
df_filtered = df[df['集客业务级别'] == 'AAA']

# 2. 告警标题不包含“衍生告警”，但是包含“业务中断”和“专线阻断”的保留
df_filtered = df_filtered[
    ~df_filtered['告警标题'].str.contains('衍生告警') |
    df_filtered['告警标题'].str.contains('业务中断|专线阻断')
]

# 3. 按照列“集客客户编码/名称”进行去重
df_filtered = df_filtered.drop_duplicates(subset='集客客户编码/名称')

# 4. 按照列“电路代号”进行去重
df_filtered = df_filtered.drop_duplicates(subset='电路代号')

# 导出筛选后的结果为 Excel 文件
output_file_path = 'E:/筛选结果.xlsx'
df_filtered.to_excel(output_file_path, index=False)

# 统计“地市名称”的数量
city_counts = df_filtered.groupby('地市名称').size().reset_index(name='数量')

# 添加“合计”行，统计总数量
total_count = city_counts['数量'].sum()
city_counts = city_counts.append({'地市名称': '合计', '数量': total_count}, ignore_index=True)
print(city_counts)

# 导出统计结果为 Excel 文件
output_stat_path = 'E:/地市统计结果.xlsx'
city_counts.to_excel(output_stat_path, index=False)

