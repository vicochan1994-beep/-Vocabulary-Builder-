import json
import random
import os
from datetime import datetime

def main():
    # Load word list
    try:
        with open('word_list.json', 'r') as f:
            words = json.load(f)
    except FileNotFoundError:
        print("Error: word_list.json not found.")
        return

    # Select 5 random words (or fewer if list is small)
    num_words = min(5, len(words))
    selected_words = random.sample(words, num_words)

    # Generate Markdown content
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = f"每日单词挑战 (Daily Vocab Challenge) - {date_str}"
    
    body = f"""
# 🎓 {date_str} 每日单词挑战

Boss，今天的 5 个单词来了。请在下方评论区 **造句打卡**，完成后关闭此 Issue。

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

    # Output for GitHub Actions
    # In a real environment, we would use environment files to set outputs
    # For now, we print to stdout or write to a file that the Action can read
    print(f"::set-output name=TITLE::{title}")
    
    # Writing body to a file to handle multiline content safely for Actions
    with open('issue_body.md', 'w') as f:
        f.write(body)

if __name__ == "__main__":
    main()
