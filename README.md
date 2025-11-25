# TalentLens

[![Status](https://img.shields.io/badge/status-operational-brightgreen)](https://img.shields.io/badge/status-operational-brightgreen)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://img.shields.io/badge/python-3.9+-blue)
[![License](https://img.shields.io/badge/license-MIT-green)](https://img.shields.io/badge/license-MIT-green)

**Note:** For the best experience with the Streamlit demo, we recommend viewing it in a browser with dark mode enabled.

## 🚀 Important Links

### 🎥 Demo Video

<a href="https://vimeo.com/1140349958">
  <img src="./ThumbnailVimeo.png" alt="TalentLense Demo" width="600"/>
</a>

### 🔹 **Live Demo (Streamlit App)**  
👉 https://talentlens-cimdbqsshfd37ja45o6mke.streamlit.app/

## Overview
TalentLens is an AI-powered recommendation engine designed to streamline the process of selecting SHL assessments for specific job roles. By leveraging natural language processing and semantic search, it helps HR professionals quickly identify the most relevant tests from SHL's extensive catalog, reducing manual effort and improving hiring efficiency.

### The Challenge
HR teams often face difficulties in aligning job requirements with the right SHL assessments. This mismatch can lead to prolonged hiring cycles, suboptimal candidate evaluations, and increased operational costs.

### Our Approach
TalentLens addresses this by automating the discovery process: it scrapes SHL's product catalog, converts assessment descriptions into vector embeddings using NLP techniques, performs semantic matching against job descriptions, and delivers tailored recommendations along with actionable HR insights.

## Technology Stack
- **Backend:** FastAPI with Uvicorn for robust API handling
- **AI and Machine Learning:** ChromaDB for vector storage and retrieval, Sentence-Transformers for embedding generation
- **Natural Language Processing:** Gemini API for generating concise insights
- **Data Scraping:** BeautifulSoup and Requests for reliable web extraction
- **Frontend:** Streamlit for an intuitive user interface
- **Deployment:** Render for API hosting and Streamlit Cloud for the demo application

## How It Works
The system follows a structured pipeline to ensure reliable and scalable performance:

1. **Data Collection:** We scrape SHL's website to gather assessment details and store them in a structured JSON format (handled in `scraper.py`).
2. **Vector Database Setup:** Descriptions are transformed into embeddings and persisted in ChromaDB for efficient querying (via `rag.py`).
3. **API Processing:** User-submitted job descriptions are analyzed to retrieve and rank relevant assessments (in `api.py`).
4. **Insight Generation:** The Gemini API evaluates the top matches to produce summaries on key skills, job level suitability, and practical usage advice.
5. **User Interface:** The frontend accepts job descriptions as input and presents ranked recommendations with embedded insights and tips.

## Workflow
``` mermaid
graph TB
    %% INITIALIZATION %%
    Start[Start System] --> Config[Initialize Configurations]
    
    %% DATA PREPARATION %%
    Config --> PrepPhase[DATA PREPARATION PHASE]
    PrepPhase --> Row1A[Scrape SHL Website]
    PrepPhase --> Row1B[Clean & Preprocess Data]
    PrepPhase --> Row1C[Store as JSON]
    Row1A --> Row2A[Generate Embeddings]
    Row1B --> Row2A
    Row1C --> Row2A
    Row2A --> Row2B[Store in ChromaDB]
    Row2B --> Row2C[Index & Sync]
    
    %% USER INTERACTION %%
    Row2C --> QueryPhase[USER INTERACTION PHASE]
    QueryPhase --> Row3A[Receive Query]
    QueryPhase --> Row3B[Preprocess Query]
    QueryPhase --> Row3C[Generate Query Embedding]
    Row3A --> Row4A[Semantic Search]
    Row3B --> Row4A
    Row3C --> Row4A
    Row4A --> Row4B[Rank Top-N Matches]
    
    %% INSIGHTS %%
    Row4B --> InsightPhase[AI INSIGHTS PHASE]
    InsightPhase --> Row5A[Send to Gemini API]
    InsightPhase --> Row5B[Generate AI Insights]
    Row5A --> End[Display Results]
    Row5B --> End
    
    %% STYLING %%
    style Start fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style Config fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style PrepPhase fill:#f3e5f5,stroke:#8e24aa,stroke-width:3px
    style QueryPhase fill:#fce4ec,stroke:#c2185b,stroke-width:3px
    style InsightPhase fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    style Row1A fill:#e8f5e9,stroke:#43a047,stroke-width:2px
    style Row1B fill:#e8f5e9,stroke:#43a047,stroke-width:2px
    style Row1C fill:#e8f5e9,stroke:#43a047,stroke-width:2px
    style Row2A fill:#f1f8e9,stroke:#7cb342,stroke-width:2px
    style Row2B fill:#f1f8e9,stroke:#7cb342,stroke-width:2px
    style Row2C fill:#f1f8e9,stroke:#7cb342,stroke-width:2px
    style Row3A fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px
    style Row3B fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px
    style Row3C fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px
    style Row4A fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style Row4B fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style Row5A fill:#fff8e1,stroke:#fdd835,stroke-width:2px
    style Row5B fill:#fff8e1,stroke:#fdd835,stroke-width:2px
    style End fill:#ffebee,stroke:#e53935,stroke-width:2px
```

## Core Features
- **Semantic Search Capabilities:** Matches job requirements to assessments using vector similarity for precise, context-aware recommendations.
- **AI-Generated Insights:** Provides succinct overviews of required skills, ideal candidate levels, and implementation guidance to support HR decision-making.
- **Production-Ready Deployment:** Built with free-tier hosting in mind, ensuring easy access without complex setup.

## Development Insights
During implementation, we encountered a few hurdles and addressed them as follows:
- **Handling Complex Scraping:** Multi-level page navigation was managed through targeted selectors and error-resilient parsing.
- **API Rate Limits:** Cohere's free tier constraints were mitigated by implementing token limits to maintain response quality.
- **Database Path Issues:** ChromaDB initialization errors in deployed environments were resolved by switching to absolute file paths.

## Getting Started
### API Access
The recommendation endpoint is live and ready for integration.

**Endpoint URL:** [https://shl-assessment-recommendor.onrender.com/recommend](https://shl-assessment-recommendor.onrender.com/recommend)

**Example Request (JSON):**
```json
{
  "text": "We want to hire a Python expert!!"
}
```

**Example Response (JSON):**
```json
{
  "name": "Python (New)",
  "url": "https://www.shl.com/solutions/products/product-catalog/view/python-new/",
  "score": 0.9339699149131775,
  "ai_insights": "1. Key skills: Programming, databases, libraries\n\n2. Job level fit: Intermediate, experienced\n\n3. Usage tip: Prepare for the assessment……"
}
```

### Interactive Demo
Explore the full user interface via our hosted Streamlit app:  
[https://shl-assessment-recommendor-v75xtfd7tsh3rxqucbedlk.streamlit.app/](https://shl-assessment-recommendor-v75xtfd7tsh3rxqucbedlk.streamlit.app/)

## Screenshots
<img width="2878" height="1460" alt="Screenshot 2025-11-23 120430" src="https://github.com/user-attachments/assets/94a10fb1-1dda-4dc5-829c-7cafc8eca3dc" />
<img width="2876" height="1457" alt="Screenshot 2025-11-23 120440" src="https://github.com/user-attachments/assets/40871871-fc0f-40cd-9386-b487a26d1b93" />
<img width="2879" height="1462" alt="Screenshot 2025-11-23 120505" src="https://github.com/user-attachments/assets/235d1fea-9bcf-4764-b97d-a9c00867261f" />
<img width="2872" height="1467" alt="Screenshot 2025-11-23 120514" src="https://github.com/user-attachments/assets/1caff11f-f8da-44ea-80fd-0011ef4c0fde" />
<img width="2875" height="1463" alt="Screenshot 2025-11-23 120533" src="https://github.com/user-attachments/assets/af5ff160-f567-465a-92a8-8be9df84cb70" />
<img width="2879" height="1447" alt="Screenshot 2025-11-23 120553" src="https://github.com/user-attachments/assets/308f0a42-61d3-4a79-81b7-1a6dc9c76624" />
<img width="2877" height="1460" alt="Screenshot 2025-11-23 120612" src="https://github.com/user-attachments/assets/183a73cc-1e76-48e1-8c9f-af97ae948532" />
<img width="2857" height="1618" alt="Screenshot 2025-11-23 120749" src="https://github.com/user-attachments/assets/e793e33b-9887-409d-9516-cf20b608f40c" />


## Business Impact
This tool has the potential to cut HR assessment selection time by up to 80%, enabling faster and more accurate hiring decisions. Its cloud-based architecture supports scalability, positioning it as a valuable asset for optimizing talent acquisition workflows.




