from langchain.tools import tool
import requests 
from bs4 import BeautifulSoup 
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient (api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic .Returns Titles, URLs and Snippets on a topics"""
    results = tavily.search(query=query,max_results=5)

    out =[]

    for r in results['results']:
        out.append(
            f'Title: {r["title"]}\nURL: {r["url"]}\nSnippet: {r["content"][:300]}\n\n'
        )

    return "\n-------\n".join(out)
print(web_search.invoke("what are the recent news of wars?"))

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text from  a given url for deeper reading."""
    try:
        resp = requests.get(url,timeout=8,headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style" "nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
     return f"could not scrape URL: {str(e)}"
    
     print(scrape_url.invoke("https://www.google.com/search?q=crickit&sca_esv=34651f0857a3a838&sxsrf=APpeQnudj_8WaLKTvzpFRvA4vdp4KCv7Fw%3A1792508964772&ei=JITXavbMLpKaseMP9JbrkQ8&biw=1360&bih=633&uact=5&oq=crickit&gs_lp=Egxnd3Mtd2l6LXNlcnAaAhgCIgdjcmlja2l0MhEQABiABBiKBRiRAhixAxiDATILEAAYgAQYigUYkQIyCxAAGIAEGIoFGJECMgsQABiABBiKBRiRAjIFEAAYgAQyDBAAGIAEGAoYCxixAzIMEAAYgAQYChgLGLEDMgUQABiABDIMEAAYgAQYChgLGLEDMgUQABiABEi8OlDxAljQK3ACeACQAQSYAeUBoAGkEaoBBjAuMTEuMbgBA8gBAPgBAZgCCaACoA2oAhTCAgQQIxgnwgINEAAYgAQYigUYQxi0B8ICBhAAGBYYHsICCBAAGBYYHhgKwgIHECMY6gIYJ8ICBxAuGOoCGCfCAhAQABgDGI8BGOoCGLQC2AEBwgINEAAYgAQYigUYQxixA8ICDRAjGKIHGJ4GGPAFGCfCAhMQLhiABBiKBRhDGMcBGK8BGI4FwgIQEAAYgAQYigUYQxixAxiDAcICDRAuGIAEGIoFGEMYsQPCAg4QABiABBiKBRiRAhiLA8ICEBAAGIAEGIoFGEMYsQMYiwPCAgsQABiABBixAxiLA8ICDRAAGIAEGBQYhwIYiwPCAhMQLhiABBiKBRhDGIsDGKgDGJsDwgINEAAYgAQYAhjLARiLA8ICDhAuGIAEGLQHGMcBGK8BwgIIEAAYgAQYtAfCAgoQABiABBgCGMsBmAMQ8QVC7NGPxfPae4gGAboGBggBEAEYCpIHBTEuNC40oAeLZbIHBTAuNC40uAePDcIHBTMtNy4yyAeRAYAIAQ&sclient=gws-wiz-serp"))