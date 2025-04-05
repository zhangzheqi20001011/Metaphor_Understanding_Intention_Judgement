import pandas as pd

# 读取CSV文件
file_path = r'.\cmt\data\data-soft.csv'
df = pd.read_csv(file_path)

# 转换正确率为浮点数
for col in ["被试理解正确率", "GPT1正确率", "GPT2正确率", "GPT3正确率"]:
    df[col] = df[col].str.replace('%', '').astype(float) / 100

# 定义计算各组内准确率的函数
def calculate_metrics(group):
    results = {
        "GPT1平均准确率": group["GPT1正确率"].mean(),
        "GPT2平均准确率": group["GPT2正确率"].mean(),
        "GPT3平均准确率": group["GPT3正确率"].mean(),
        "被试平均理解正确率": group["被试理解正确率"].mean()
    }
    return results

# 按条件分组计算
def group_and_calculate(df, filter_conditions, group_name):
    filtered_group = df.copy()
    for col, val in filter_conditions.items():
        filtered_group = filtered_group[filtered_group[col] == val]
    return group_name, calculate_metrics(filtered_group)

# 定义分组条件
groups_conditions = [
    ({"身体/情感特异性": 1}, "身体/情感特异性句子"),
    ({"文化特异性": 1}, "文化特异性句子"),
    ({"体裁": 1}, "体裁为1的句子"),
    ({"体裁": 2}, "体裁为2的句子"),
    *[
        ({"隐喻类型（0-非隐喻句 1- 词汇化隐喻 2-常规隐喻 3-新奇隐喻）": i}, f"隐喻类型为{i}的句子")
        for i in range(0, 4)
    ]
]

# 计算并输出结果
results = {}
for conditions, name in groups_conditions:
    group_name, group_results = group_and_calculate(df, conditions, name)
    results[group_name] = group_results

# 转为DataFrame展示
results_df = pd.DataFrame(results).T
print(results_df)
