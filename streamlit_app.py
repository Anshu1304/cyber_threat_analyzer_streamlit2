import streamlit as st
from gpt_helper2 import GPTHelper
from database import ThreatDatabase
from NewsScraper import NewsScraper  # Corrected import
import datetime

st.set_page_config(page_title="Cyber Threat Analyzer", layout="wide")
st.title("🛡️ Cyber Threat Analyzer")
st.markdown("Analyze and tag cyber threats using AI (Gemma model via OpenRouter)")

gpt = GPTHelper()
db = ThreatDatabase()
news_scraper = NewsScraper()  # Corrected instantiation

# Function to compare GPT and News Scraper data
def compare_data(gpt_data, news_data):
    gpt_date_str = gpt_data.get('created_at')
    news_date_str = news_data.get('publishedAt')

    if not gpt_date_str or not news_date_str:
        return "Unable to compare dates: Missing date information"

    try:
        gpt_date = datetime.datetime.strptime(gpt_date_str, '%Y-%m-%dT%H:%M:%S.%f')
        news_date = datetime.datetime.strptime(news_date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError as e:
        return f"Error parsing dates: {e}"

    if gpt_date > news_date:
        return "GPT data is more recent"
    else:
        return "News Scraper data is more recent"

option = st.sidebar.radio(
    "Select an action:",
    ["🔍 Analyze Threat", "🏷️ Tag Threat Data"]
)

if option == "🔍 Analyze Threat":
    st.header("🔍 Threat Analysis")
    query = st.text_area("Enter threat description to analyze:")
    if st.button("Analyze"):
        with st.spinner("Analyzing threat data using AI..."):
            gpt_result = gpt.analyze_threat(query)
            st.subheader("📌 AI Response")
            st.write(gpt_result)
else:
                st.write("No relevant articles found for comparison.")

elif option == "🏷️ Tag Threat Data":
    st.header("🏷️ Threat Tagger")
    data = st.text_area("Enter raw threat data to tag:")
    if st.button("Tag"):
        with st.spinner("Tagging data using AI..."):
            tagging_result = gpt.tag_threat_data(data)
            st.subheader("📌 Tagged Result")
            st.json(tagging_result)
st.markdown("---")
    db.save_threat(data, str(result["data"]))
