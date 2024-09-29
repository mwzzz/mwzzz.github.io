import pandas as pd

# 创建一个示例 DataFrame
data = {
    '姓名': ['小明', '小华', '小李', '小红'],
    '性别': ['男', '男', '男', '女'],
    '年龄': [25, 30, 35, 28],
    '分数': [90, 85, 82, 88]
}

df = pd.DataFrame(data)
print("原始 DataFrame:")
print(df)

# 使用 value_counts() 统计 性别 列中每个性别的数量
gender_counts = df['性别'].value_counts()
print("\n使用 value_counts() 统计 性别 列的数量:")
print(gender_counts)

# 使用 groupby 和 size 统计 性别 列中每个性别的数量
gender_grouped_counts = df.groupby('性别').size().reset_index(name='数量')
print("\n使用 groupby 和 size 统计 性别 列的数量:")
print(gender_grouped_counts)

# 使用 groupby 和 size 统计 年龄 列中每个年龄的数量
age_grouped_counts = df.groupby('年龄').size().reset_index(name='数量')
print("\n使用 groupby 和 size 统计 年龄 列的数量:")
print(age_grouped_counts)