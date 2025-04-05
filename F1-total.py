import pandas as pd

# 读取CSV文件
file_path = r'.\cmt\data\data.csv'
df = pd.read_csv(file_path)

# 转换正确率为浮点数
for col in ["被试理解正确率", "GPT1正确率", "GPT2正确率", "GPT3正确率"]:
    df[col] = df[col].str.replace('%', '').astype(float) / 100

results = []

# 计算总体的 TP、FP 和 FN
TN_human, TP_human, FP_human, FN_human = 0, 0, 0, 0
TN_gpt1, TP_gpt1, FP_gpt1, FN_gpt1 = 0, 0, 0, 0
TN_gpt2, TP_gpt2, FP_gpt2, FN_gpt2 = 0, 0, 0, 0
TN_gpt3, TP_gpt3, FP_gpt3, FN_gpt3 = 0, 0, 0, 0

# 统一统计
for name, group in df.groupby('隐喻类型'):
    if name == 0:  # 无隐喻
        TN_human += (group['被试理解正确率'] == 1).sum()/len(group)
        FN_human += (group['被试理解正确率'] == 0).sum()/len(group)
        
        
        TN_gpt1 += (group['GPT1正确率'] == 1).sum()/len(group)
        FN_gpt1 += (group['GPT1正确率'] == 0).sum()/len(group)
        
        TN_gpt2 += (group['GPT2正确率'] == 1).sum()/len(group)
        FN_gpt2 += (group['GPT2正确率'] == 0).sum()/len(group)

        TN_gpt3 += (group['GPT3正确率'] == 1).sum()/len(group)
        FN_gpt3 += (group['GPT3正确率'] == 0).sum()/len(group)
        
    else:  # 有隐喻
        TP_human += (group['被试理解正确率'] == 1).sum()/len(group)
        FP_human += (group['被试理解正确率'] == 0).sum()/len(group)
        
        
        TP_gpt1 += (group['GPT1正确率'] == 1).sum()/len(group)
        FP_gpt1 += (group['GPT1正确率'] == 0).sum()/len(group)
        
        TP_gpt2 += (group['GPT2正确率'] == 1).sum()/len(group)
        FP_gpt2 += (group['GPT2正确率'] == 0).sum()/len(group)
        
        TP_gpt3 += (group['GPT3正确率'] == 1).sum()/len(group)
        FP_gpt3 += (group['GPT3正确率'] == 0).sum()/len(group)

# 计算精确率和召回率
def calculate_metrics(TP, FP, FN):
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

# 计算人类的指标
precision_human, recall_human, f1_human = calculate_metrics(TP_human, FP_human, FN_human)

# 计算GPT1的指标
precision_gpt1, recall_gpt1, f1_gpt1 = calculate_metrics(TP_gpt1, FP_gpt1, FN_gpt1)

# 计算GPT2的指标
precision_gpt2, recall_gpt2, f1_gpt2 = calculate_metrics(TP_gpt2, FP_gpt2, FN_gpt2)

# 计算GPT3的指标
precision_gpt3, recall_gpt3, f1_gpt3 = calculate_metrics(TP_gpt3, FP_gpt3, FN_gpt3)

# 输出结果
results.append({
    '模型': '人类',
    '精确率': precision_human,
    '召回率': recall_human,
    'F1值': f1_human,
    'TP':TP_human,
    'FP': FP_human,
    'FN': FN_human
    
})

results.append({
    '模型': 'GPT1',
    '精确率': precision_gpt1,
    '召回率': recall_gpt1,
    'F1值': f1_gpt1,
    'TP':TP_gpt1,
    'FP': FP_gpt1,
    'FN': FN_gpt1
})

results.append({
    '模型': 'GPT2',
    '精确率': precision_gpt2,
    '召回率': recall_gpt2,
    'F1值': f1_gpt2,
    'TP':TP_gpt2,
    'FP': FP_gpt2,
    'FN': FN_gpt2
})

results.append({
    '模型': 'GPT3',
    '精确率': precision_gpt3,
    '召回率': recall_gpt3,
    'F1值': f1_gpt3,
    'TP':TP_gpt3,
    'FP': FP_gpt3,
    'FN': FN_gpt3
})

# 转换结果为DataFrame以便查看
results_df = pd.DataFrame(results)
print(results_df)
