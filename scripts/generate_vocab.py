import json
import random
import os
from datetime import datetime

def main():
    # Load word list
    # Determine the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # The word list is in the parent directory
    file_path = os.path.join(script_dir, '..', 'word_list.json')
    
    try:
        with open(file_path, 'r') as f:
            words = json.load(f)
    except FileNotFoundError:
        print(f"Error: word_list.json not found at {file_path}")
        return

    # Select 5 random words (or fewer if list is small)
    num_words = min(5, len(words))
    selected_words = random.sample(words, num_words)

    # Generate Markdown content
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = f"每日单词挑战 (Daily Vocab Challenge) - {date_str}"
    
    body = f"""
# 🌱 {date_str} 每日口语积累 (Daily Speaking)

Boss，收到！我们的目标是 **5 个月后流利对话**。
今天是 **第 1 阶段 - 生存英语 (Survival English)**。
请大声朗读下面的例句，并在评论区模仿造句。

---

"""

    for i, word_data in enumerate(selected_words, 1):
        body += f"""
## {i}. **{word_data['word']}** ({word_data['part_of_speech']})
> *{word_data['definition']}*

*   **Example**: {word_data['example']}
*   **Your Turn**: ______

"""

    body += """
---
**任务**: 
1. 复制每个单词，在评论区写一个包含该单词的句子。
2. 完成后点击 "Close issue"。
**坚持把这堆单词吃透！** 
"""

    # Output for GitHub Actions using GITHUB_OUTPUT
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"TITLE={title}\n")
    
    # Writing body to a file
    with open('issue_body.md', 'w') as f:
        f.write(body)

if __name__ == "__main__":
    main()
