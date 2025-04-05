import re
if __name__ == '__main__':
    # 原始多行文本
    text = """
    """

    lines = text.split('\n')

    # 使用正则表达式移除每行开头的序号和点
    cleaned_lines = [re.sub(r"^\d+\.\s*", "", line) for line in lines]

    # 合并清理后的文本
    cleaned_text = '\n'.join(cleaned_lines)
    # 打印结果

    with open('cleaned_text.txt', 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
    print(cleaned_text)
