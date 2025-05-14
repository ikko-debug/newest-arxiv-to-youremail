# newest-arxiv-to-youremail
## 📡 ArXiv Mamba/SSM 新论文日报系统

一个基于 Python 脚本的自动化工具，实时追踪 arXiv 上与 **Mamba**、**State Space Model (SSM)** 相关的新论文，自动获取英文摘要，调用百度翻译 API 翻译为中文，并检测该论文是否在 Papers with Code 上有开源实现，最终将整理好的日报以 HTML 格式邮件推送到你的邮箱。

---

## ✨ 功能亮点

- 🔍 **关键词追踪**：多关键词 arXiv 论文实时检索  
- 📖 **中英文双语摘要**：调用百度翻译 API，自动翻译英文摘要为中文  
- 📝 **代码开源检测**：查询论文是否在 [Papers with Code](https://paperswithcode.com) 有代码实现  
- 📧 **HTML 精美邮件推送**：自动生成日报，发送至指定邮箱  
- 📆 **可定时任务触发**：支持 crontab 等定时器定时执行  

---

## 📦 项目目录结构
├── config.json # 邮箱与 API 配置（可选）
├── daily_paper_report.py # 主程序
├── requirements.txt # 依赖库
└── README.md # 项目说明文档

---

## 📥 安装依赖

```bash
pip install -r requirements.txt
```
## ⚙️ 配置说明
smtp_server = 'smtp.qq.com'
smtp_port = 587
sender_email = '你的邮箱@qq.com'
sender_password = '你的授权码'
receiver_email = '接收方邮箱'

appid = '你的百度翻译APP ID'
secret_key = '你的密钥'

## 🚀 使用方法
直接运行
```bash
python arxiv_daily_report.py
```
📅 配置定时任务（Linux crontab 示例）
```bash
0 9 * * * /usr/bin/python3 /你的路径/arxiv_daily_report.py
```
查看定时任务：
```bash
crontab -l
```
📬 邮件效果示意

英文摘要 ✅
中文翻译 ✅
论文链接 ✅
是否开源实现 ✅
截图：

