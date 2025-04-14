import streamlit as st
from gpt_helper2 import GPTHelper
from database import ThreatDatabase
from NewsScraper import NewsScraper
import datetime

st.set_page_config(page_title="Cyber Threat Analyzer", layout="wide")
st.title("🛡️ Cyber Threat Analyzer")
st.markdown("Analyze and tag cyber threats using AI and real-time news")

gpt = GPTHelper()
db = ThreatDatabase()
news_scraper = NewsScraper()

# Function to compare GPT and News Scraper data
def compare_data(gpt_data, news_data):
    gpt_date = datetime.datetime.strptime(gpt_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
    news_date = datetime.datetime.strptime(news_data['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    
    if gpt_date > news_date:
        return "GPT data is more recent"
    else:
        return "News Scraper data is more recent"

option = st.sidebar.radio(
    "Select an action:",
    ["🔍 Analyze Threat", "🏷️ Tag Threat Data", "📰 Fetch News"]
)

if option == "🔍 Analyze Threat":
    st.header("🔍 Threat Analysis")
    query = st.text_area("Enter threat description to analyze:")
    if st.button("Analyze"):
        with st.spinner("Analyzing threat data using AI..."):
            gpt_result = gpt.analyze_threat(query)
            st.subheader("📌 AI Response")
            st.write(gpt_result)

            # Fetch news and compare
            news_articles = news_scraper.fetch_articles(query, page_size=1)
            if news_articles:
                news_data = news_articles[0]
                comparison_result = compare_data(gpt_result, news_data)
                st.write(f"Comparison: {comparison_result}")
            else:
                st.write("No news articles found for comparison.")

elif option == "🏷️ Tag Threat Data":
    st.header("🏷️ Threat Tagger")
    data = st.text_area("Enter raw threat data to tag:")
    if st.button("Tag"):
        with st.spinner("Tagging data using AI..."):
            tagging_result = gpt.tag_threat_data(data)
            st.subheader("📌 Tagged Result")
            st.json(tagging_result)

elif option == "📰 Fetch News":
    st.header("📰 Fetch Real-Time News")
    news_query = st.text_input("Enter query for news articles:")
    if st.button("Fetch News"):
        with st.spinner("Fetching news articles..."):
            news_articles = news_scraper.fetch_articles(news_query, page_size=3)  # Fetch 3 articles
            if news_articles:
                for article in news_articles:
                    st.subheader(article.get('title', 'No title'))
                    st.write(f"Author: {article.get('author', 'Unknown')}")
                    st.write(f"Published at: {article.get('publishedAt', 'N/A')}")
                    st.write(f"Description: {article.get('description', 'No description')}")
                    st.write(f"URL: {article.get('url', 'N/A')}")
                    st.markdown("---")
            else:
                st.write("No relevant articles found.")
