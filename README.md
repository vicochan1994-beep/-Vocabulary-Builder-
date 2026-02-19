# 部署指南：每日单词 (Vocabulary Builder)

Boss，你的 "强制学习机" 已经准备好了。
按以下步骤操作，5 分钟内部署上线：

## 1. 准备仓库
在你的 GitHub 上新建一个仓库（Repository），名字比如叫 `my-daily-vocab`。

## 2. 上传文件
把这个文件夹里的内容原样复制进去，保持以下结构：
```text
.
├── .github
│   └── workflows
│       └── daily_vocab.yml   <-- 自动化流水线
├── scripts
│   └── generate_vocab.py     <-- 生成脚本
├── word_list.json            <-- 单词库 (你可以随时加新词)
└── README.md
```

## 3. 启用权限
为了让机器人能发 Issue，你需要检查仓库设置：
1. 进入 `Settings` -> `Actions` -> `General`。
2. 找到 `Workflow permissions`。
3. 勾选 **"Read and write permissions"**。
4. Save。

## 4. 测试
1. 进入 `Actions` 标签页。
2. 左侧点击 `Vocabulary Builder Daily`。
3. 点击右侧 `Run workflow` 按钮手动跑一次。

4.  **Done!** 坐等 Issue 来敲门。
以后每天早上 8 点（北京时间），它都会准时来催你背单词。

---
**进阶玩法**：
*   你可以编辑 `word_list.json`，把你想背的词（GRE/雅思/技术名词）加进去。
*   嫌 JSON 麻烦？告诉我，我帮你改成从 API 抓取（比如由我每天自动生成 5 个新词）。

## ❓ 常见问题 (Troubleshooting)

### Q: 机器人报错 "402 Payment Required"？
**A: 你的 DeepSeek API 余额不足。**
*   请前往 [DeepSeek 控制台](https://platform.deepseek.com/) 充值（通常几块钱就够用很久）。
*   充值后，无需修改代码，直接在 Issue 下面重新评论即可触发。

### Q: 机器人没反应？
*   检查 GitHub Actions 页面，看看 workflow 是否绿色。
*   如果是红色，点进去看报错日志。
*   检查 `LLM_API_KEY` 是否配置正确 (需在 Secrets 里配置，而不是 Variables)。
