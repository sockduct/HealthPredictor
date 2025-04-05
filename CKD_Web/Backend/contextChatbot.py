import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import requests
from bs4 import BeautifulSoup

# Load env variables
load_dotenv('.env')

# Load context from local file
def load_local_context(filename='context.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "No context loaded."

def scrape_websites(urls):
    scraped_content = []
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text from the webpage
            paragraphs = soup.find_all('p')  
            page_text = "\n".join(p.get_text(strip=True) for p in paragraphs[:15])

            if page_text:
                scraped_content.append(f"Content from {url}:\n{page_text}\n")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")

    return "\n".join(scraped_content)

# Combine local file context and web-scraped content
def get_combined_context(urls):
    local_context = load_local_context()
    web_content = scrape_websites(urls)
    combined_context = f"Local Context:\n{local_context}\n\nWeb Context:\n{web_content}"
    return combined_context

urls = [
    "https://www.hopkinsmedicine.org/health/conditions-and-diseases/chronic-kidney-disease", 
    "https://medlineplus.gov/ency/article/000471.htm",
    "https://www.kidney.org/kidney-topics/understanding-your-lab-values-and-other-ckd-health-numbers"
]
general_context = get_combined_context(urls)

# Init Azure OpenAI
llm = AzureChatOpenAI(
    deployment_name=os.environ['MODEL'],
    openai_api_version=os.environ['API_VERSION'],
    openai_api_key=os.environ['OPENAI_API_KEY'],
    azure_endpoint=os.environ['OPENAI_API_BASE'],
    openai_organization=os.environ['OPENAI_ORGANIZATION']
)

