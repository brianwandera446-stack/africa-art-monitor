"""
AFRICA ARTIST NEWS MONITOR v1.0
Monitors 20+ RSS feeds for African artist news → Email alerts
"""

import feedparser
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import sys

# Import our classifier (same folder)
from classify import classify

# RSS feeds with African art coverage
RSS_FEEDS = [
    "https://www.artforum.com/feed/rss/",
    "https://www.theartnewspaper.com/rss.xml", 
    "https://news.artnet.com/art-world/feed",
    "https://www.artnews.com/feed/rss/",
    "https://artafricamagazine.org/feed/",
    "https://feeds.hyperallergic.com/hyperallergic",
    "https://www.theguardian.com/artanddesign/art/rss",
    "https://www.africanews.com/feed/rss",
]

# YOUR EMAIL SETTINGS (UPDATE PASSWORD IN STEP 10)
EMAIL_FROM = "africaartnews160@gmail.com"
EMAIL_TO = "info@africaartnews.com"
PASSWORD =  "hehcjvwydyetxtmx"  # Africa Art Monitor
SMTP_SERVER = "smtp.gmail.com"

def send_email(subject, body):
    """Send alert email."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        
        with smtplib.SMTP(SMTP_SERVER, 587) as server:
            server.starttls()
            server.login(EMAIL_FROM, PASSWORD)
            server.send_message(msg)
        return True
    except:
        return False

def main():
    print("🚀 Africa Artist News Monitor Starting...")
    print(f"📧 {EMAIL_FROM} → {EMAIL_TO}")
    
    alerts = []
    
    for i, url in enumerate(RSS_FEEDS, 1):
        print(f"[{i}/{len(RSS_FEEDS)}] {url}", end=" ")
        try:
            feed = feedparser.parse(url)
            count = 0
            
            for entry in feed.entries[:5]:  # Check 5 latest
                title = entry.title
                desc = entry.get('summary', '')
                
                result = classify(title, desc)
                
                if result.relevant and result.subject == "artists":
                    alerts.append({
                        'title': title,
                        'link': entry.link,
                        'tier': result.tier,
                        'reason': result.reason
                    })
                    count += 1
            
            print(f"✅ {count} artists found")
            
        except Exception as e:
            print(f"❌ error")
    
    # Send email if alerts found
    if alerts:
        body = f"AFRICA ARTIST NEWS ALERTS ({len(alerts)} found)\n\n"
        for alert in alerts:
            body += f"Tier {alert['tier']}: {alert['title']}\n"
            body += f"{alert['reason']}\n"
            body += f"{alert['link']}\n\n"
        
        if send_email(f"{len(alerts)} African Artist Alerts", body):
            print("✅ EMAIL SENT!")
        else:
            print("❌ EMAIL FAILED - check password")
    else:
        print("ℹ️ No new African artist news today")

if __name__ == "__main__":
    main()
