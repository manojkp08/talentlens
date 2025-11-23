from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from bs4 import BeautifulSoup
import requests
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize Gemini directly (not via LangChain to avoid auth issues)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = genai.GenerativeModel('gemini-2.0-flash')

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.PersistentClient(path="app/chroma_db")

class QueryRequest(BaseModel):
    text: str
    use_ai: bool = True

def scrape_job_description(url: str) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=50)
        soup = BeautifulSoup(response.text, "html.parser")
        job_desc_div = soup.select_one("div.job-description, section.description")
        return job_desc_div.get_text(" ", strip=True) if job_desc_div else ""
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraping error: {str(e)}")
    
def normalize_score(score: float) -> float:
    try:
        return max(0.0, min(1.0, abs(float(score))))
    except:
        return 0.5

def generate_gemini_insights(description: str) -> str:
    if not llm:
        return "AI insights unavailable"
    
    try:
        prompt = f"""As an HR expert, analyze this assessment description and provide 3 concise insights:
        
        Description: {description[:300]}
        
        Format as:
        1. Key skills measured
        2. Ideal candidate level
        3. Best use case"""
        
        response = llm.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5,
                max_output_tokens=150
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return "AI insights unavailable"

@app.post("/recommend")
async def recommend(request: QueryRequest):
    try:
        collection = chroma_client.get_collection("shl_assessments")
    except ValueError:
        raise HTTPException(status_code=500, detail="Vector DB not initialized")

    query_text = request.text
    if query_text.startswith(("http://", "https://")):
        query_text = scrape_job_description(query_text)

    results = collection.query(
        query_texts=[query_text],
        n_results=10,
        include=["metadatas", "documents", "distances"]
    )

    recommendations = []
    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]
        recommendations.append({
            "name": metadata["name"],
            "url": metadata["url"],
            "description": metadata["description"],
            "duration": metadata.get("duration", "Not specified"),
            "languages": metadata.get("languages", []),
            "job_level": metadata.get("job_level", "Not specified"),
            "remote_testing": metadata.get("remote_testing", "❓"),
            "adaptive_support": metadata.get("adaptive/irt_support", "❓"),
            "test_type": metadata.get("test_type", "Not specified"),
            "score": normalize_score(results["distances"][0][i]),
            "ai_insights": generate_gemini_insights(metadata["description"]) if request.use_ai else ""
        })

    return recommendations