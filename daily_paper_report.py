import feedparser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from urllib.parse import quote
import hashlib
import random
import json
import os

# 读取 config.json 配置
with open('./newest-arxiv-to-youremail/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 邮箱配置
smtp_server = config['smtp_server']
smtp_port = config['smtp_port']
sender_email = config['sender_email']
sender_password = config['sender_password']
receiver_email = config['receiver_email']

# 百度翻译配置
appid = config['appid']
secret_key = config['secret_key']
api_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

# 获取关键词和RSS源
keywords = config['keywords']
rss_url = config['rss_url']

def search_arxiv():
    result_list = []
    for keyword in keywords:
        query_url = rss_url.format(quote(keyword))
        feed = feedparser.parse(query_url)
        for entry in feed.entries:
            link = entry.link
            
            result_list.append({
                "title": entry.title,
                "link": link,
                "summary": entry.summary
            })
    return result_list


def check_paperswithcode(paper_title):
    url = f"https://paperswithcode.com/api/v1/papers/?q={paper_title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            return True
    return False

def send_email(content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr(("论文追踪", sender_email))
    message['To'] = formataddr(("你", receiver_email))
    message['Subject'] = Header("今日 Mamba/SSM 新论文速递", 'utf-8')

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, [receiver_email], message.as_string())
    server.quit()

def send_html_email(content):
    message = MIMEMultipart("alternative")
    message['From'] = formataddr(("论文追踪", sender_email))
    message['To'] = formataddr(("你", receiver_email))
    message['Subject'] = Header("📖 今日 Mamba/SSM 新论文日报", 'utf-8')

    html_part = MIMEText(content, 'html', 'utf-8')
    message.attach(html_part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, [receiver_email], message.as_string())
    server.quit()

def translate_to_chinese(text):
    salt = str(random.randint(32768, 65536))
    sign = appid + text + salt + secret_key
    sign = hashlib.md5(sign.encode('utf-8')).hexdigest()

    params = {
        'q': text,
        'from': 'en',
        'to': 'zh',
        'appid': appid,
        'salt': salt,
        'sign': sign
    }

    try:
        response = requests.get(api_url, params=params)
        result = response.json()
        if 'trans_result' in result:
            return result['trans_result'][0]['dst']
        else:
            return '【翻译失败】'
    except Exception as e:
        print(f"翻译出错: {e}")
        return '【翻译异常】'

# 新增：逐行翻译摘要
def translate_summary(summary_en):
    lines = summary_en.split("\n")
    translated_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        translated_line = translate_to_chinese(line.strip())
        translated_lines.append(translated_line)
    return "<br>".join(translated_lines)

if __name__ == "__main__":
    papers = search_arxiv()
    if papers:
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif;">
        <h2>📖 今日 Mamba/SSM 新论文日报</h2>
        <hr>
        """
        for paper in papers:
            title = paper['title']
            link = paper['link']
            summary_en = paper['summary']
            

            # 翻译摘要
            summary_zh = translate_summary(summary_en)
            has_code = check_paperswithcode(title)

            # arXiv 封面图地址
            arxiv_id = link.split("/")[-1]
            cover_img = f"https://arxiv.org/pdf/{arxiv_id}.pdf#page=1"

            # 替换换行符 \n 为 <br> 标签
            summary_en = summary_en.replace("\n", "<br>")
            summary_zh = summary_zh.replace("\n", "<br>")

            html_content += f"""
            <div style="margin-bottom: 20px;">
                <h3><a href="{link}" target="_blank">{title}</a></h3>
                <p><strong>是否有代码实现：</strong> {'<span style="color:green;">有✅</span>' if has_code else '<span style="color:red;">暂无❌</span>'}</p>
                <p><strong>英文摘要：</strong><br>{summary_en}</p>
                <p><strong>中文摘要：</strong><br>{summary_zh}</p>
                <p><a href="{link}" target="_blank">🔗 查看论文</a></p>
                <hr>
            </div>
            """

        html_content += "</body></html>"
        send_html_email(html_content)
    else:
        send_html_email("<h3>📭 今日无新论文更新。</h3>")
