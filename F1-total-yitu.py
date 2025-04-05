import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

# 读取CSV文件
file_path = r'.\cmt\data\data-yitu.csv'
df = pd.read_csv(file_path)

# 转换正确率为浮点数
for col in ["意图任务正确率(平均)", "意图任务正确率(多数)", "GPT意图任务正确率", "GPT正确率2", "GPT正确率3"]:
    df[col] = df[col].str.replace('%', '').astype(float) / 100

# 展开“人类评委意图评价”列中包含的多个意图类型
df["人类评委意图评价"] = df["人类评委意图评价"].astype(str)
expanded_rows = []
for _, row in df.iterrows():
    intents = row["人类评委意图评价"].split(",")  # 分割意图类型
    for intent in intents:
        new_row = row.copy()
        new_row["人类评委意图评价"] = int(intent.strip())  # 去除空格并转为整数
        expanded_rows.append(new_row)

# 构建新的DataFrame用于分组计算
expanded_df = pd.DataFrame(expanded_rows)

# 定义计算F1值的函数
def calculate_f1(group, col_name):
    # 将正确率列转为二进制标签，>=0.5的视为正确（1），<0.5视为错误（0）
    binary_labels = (group[col_name] >= 0.5).astype(int)
    true_labels = [1] * len(binary_labels)  # 假设真实标签都是1（即所有任务都期望正确）
    
    precision, recall, f1_score, _ = precision_recall_fscore_support(true_labels, binary_labels, average='binary')
    return f1_score

# 按“人类评委意图评价”分组计算F1值
results = {}
for intent_type in range(10):  # 假设意图评价为0-9
    group = expanded_df[expanded_df["人类评委意图评价"] == intent_type]
    if not group.empty:
        results[f"意图评价类型 {intent_type}"] = {
            "意图任务正确率(多数) F1": calculate_f1(group, "意图任务正确率(多数)"),
            "GPT意图任务正确率 F1": calculate_f1(group, "GPT意图任务正确率"),
            "GPT正确率2 F1": calculate_f1(group, "GPT正确率2"),
            "GPT正确率3 F1": calculate_f1(group, "GPT正确率3")
        }

# 转为DataFrame
results_df = pd.DataFrame(results).T

# 保存到Excel文件
output_file_path = r'.\cmt\results\intent_f1_scores.xlsx'
results_df.to_excel(output_file_path, index=True)

print(f"F1值结果已成功保存到 {output_file_path}")
