import pandas as pd

# 创建一个示例 DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [25, 30, 35, 22, 28],
    'Score': [90, 85, 82, 95, 88]
}

df = pd.DataFrame(data)
print("原始 DataFrame:")
print(df)

# 按索引升序排序
sorted_by_index_asc = df.sort_index()
print("\n按索引升序排序:")
print(sorted_by_index_asc)

# 按索引降序排序
sorted_by_index_desc = df.sort_index(ascending=False)
print("\n按索引降序排序:")
print(sorted_by_index_desc)

# 按 Age 升序排序
sorted_by_age_asc = df.sort_values(by='Age')
print("\n按 Age 升序排序:")
print(sorted_by_age_asc)

# 按 Score 降序排序
sorted_by_score_desc = df.sort_values(by='Score', ascending=False)
print("\n按 Score 降序排序:")
print(sorted_by_score_desc)

# 按多个列排序（先按 Age 升序，再按 Score 降序）
sorted_by_multiple_columns = df.sort_values(by=['Age', 'Score'], ascending=[True, False])
print("\n按 Age 升序和 Score 降序排序:")
print(sorted_by_multiple_columns)

# 筛选出 Age 大于 25 的行
filtered_by_age = df[df['Age'] > 25]
print("\n筛选出 Age 大于 25 的行:")
print(filtered_by_age)

# 使用 query 方法筛选出 Score 小于 90 的行
filtered_by_score = df.query('Score < 90')
print("\n使用 query 方法筛选出 Score 小于 90 的行:")
print(filtered_by_score)

# 复合条件筛选：Age 大于 25 并且 Score 小于 90
filtered_by_age_and_score = df[(df['Age'] > 25) & (df['Score'] < 90)]
print("\n复合条件筛选：Age 大于 25 并且 Score 小于 90:")
print(filtered_by_age_and_score)

# 筛选出名字中包含字符串 'a' 的行
filtered_df = df[df['Name'].str.contains('a', case=False)]
print("\n名字中包含 'a' 的行:")
print(filtered_df)
