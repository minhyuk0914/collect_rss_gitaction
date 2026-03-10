import feedparser
import os
from datetime import datetime

# 수집할 RSS 피드 리스트
FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Anthropic": "https://www.anthropic.com/index.xml",
    "Google AI": "https://blog.google/technology/ai/rss/"
}

def collect_news():
    summary_content = f"## LLM 공식 블로그 업데이트 ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    has_update = False

    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        summary_content += f"### {source}\n"
        
        # 최근 3개의 포스트만 가져오기
        entries = feed.entries[:3]
        if entries:
            has_update = True
            for entry in entries:
                summary_content += f"- [{entry.title}]({entry.link}) ({entry.published if 'published' in entry else 'Date N/A'})\n"
        else:
            summary_content += "- 최근 소식이 없습니다.\n"
        summary_content += "\n"

    # 파일 저장 (logs 폴더에 날짜별로 저장)
    os.makedirs("logs", exist_ok=True)
    filename = f"logs/update_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    # 메인 README.md 업데이트 (최신 현황 파악용)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# My LLM Knowledge Base\n\n" + summary_content)

if __name__ == "__main__":
    collect_news()
