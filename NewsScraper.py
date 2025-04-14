import requests
import time

class NewsScraper:
    def __init__(self):
        self.base_url = "https://newsapi.org/v2/everything"
        self.api_key = "014ff12200e04a4db0205d9c899e7fa6"  # Replace with your actual API key from NewsAPI
        self.headers = {"Content-Type": "application/json"}

    def fetch_articles(self, query, page_size=1):
        params = {
            'q': query,
            'apiKey': self.api_key,
            'pageSize': page_size,
            'language': 'en'
        }
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"Total results found for query '{query}': {data['totalResults']}")  # Debugging line
            if data['status'] == 'ok' and data['totalResults'] > 0:
                return data['articles']
            else:
                print(f"No relevant articles found for the query '{query}'. Please try again later or refine the query.")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def process_news_response(self, query):
        articles = self.fetch_articles(query)
        if articles:
            print(f"\nTop articles for '{query}':\n")
            for idx, article in enumerate(articles, 1):
                title = article.get('title', 'No title available')
                author = article.get('author', 'Unknown author')
                description = article.get('description', 'No description available')
                content = article.get('content', 'No content available')
                url = article.get('url', 'N/A')
                published_at = article.get('publishedAt', 'No date available')

                print(f"{idx}. {title}")
                print(f"   Author: {author}")
                print(f"   Published at: {published_at}")
                print(f"   Description: {description}")
                print(f"   Content: {content[:150]}...")  # Limiting content to first 150 chars for brevity
                print(f"   Read more: {url}\n")
        else:
            print("No relevant articles found, please try again later or change the query.\n")

    def start_scraper(self):
        print("Welcome to the real-time News Scraper!")
        print("You can select a query from the options below by typing the corresponding number.")
        print("Type 'exit' to quit the program.\n")
        while True:
            print("1. latest cybersecurity vulnerabilities")
            print("2. SQL injection attack")
            print("3. ransomware 2025")
            print("4. data breach 2025")
            print("5. AI in cybersecurity")
            print("6. cloud security breaches")
            print("7. phishing attacks trends")
            print("8. Recent Cyberattack in Australia")
            print("9. latest trends in hacking")
            print("10. cybersecurity job market")
            # Add more options as needed...

            query_choice = input("Enter a number (1-10) to select a query or type 'exit' to quit: ").strip()

            if query_choice == 'exit':
                print("Exiting the program...")
                break

            query_dict = {
                '1': 'latest cybersecurity vulnerabilities',
                '2': 'SQL injection attack',
                '3': 'ransomware 2025',
                '4': 'data breach 2025',
                '5': 'AI in cybersecurity',
                '6': 'cloud security breaches',
                '7': 'phishing attacks trends',
                '8': 'Recent Cyberattack in Australia',
                '9': 'latest trends in hacking',
                '10': 'cybersecurity job market',
                # Add more query mappings as needed...
            }

            if query_choice in query_dict:
                selected_query = query_dict[query_choice]
                self.process_news_response(selected_query)
            else:
                print("Invalid selection, please try again.\n")

if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.start_scraper()
