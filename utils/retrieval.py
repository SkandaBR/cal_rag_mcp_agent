"""
Hybrid search retrieval utility for RAG.
This is a mock implementation - replace with your actual vector DB/search logic.
"""

def hybrid_search(query: str, top_k: int = 3) -> list[str]:
    """
    Perform hybrid search (semantic + keyword) to retrieve relevant documents.
    
    Args:
        query: Search query string
        top_k: Number of top results to return
        
    Returns:
        List of relevant document strings
    """
    # Mock data - replace with actual vector DB retrieval
    mock_documents = {
        "germany renewable": [
            "Germany's renewable energy sector generated 250 TWh in 2023, representing 45% of total electricity consumption.",
            "Germany has set ambitious targets to reach 80% renewable energy by 2030 and climate neutrality by 2045.",
            "Wind and solar power are the main drivers of Germany's energy transition, with offshore wind capacity expanding rapidly."
        ],
        "renewable energy": [
            "Renewable energy sources include solar, wind, hydro, biomass, and geothermal power.",
            "Global renewable energy capacity has been growing at 10% annually over the past decade.",
            "The cost of solar and wind energy has decreased by over 80% in the last 10 years."
        ],
        "climate": [
            "Climate change mitigation requires rapid transition to renewable energy sources.",
            "The Paris Agreement aims to limit global warming to 1.5°C above pre-industrial levels.",
            "Renewable energy is key to reducing greenhouse gas emissions from the power sector."
        ]
    }
    
    # Simple keyword matching - replace with semantic search
    query_lower = query.lower()
    results = []
    
    for key, docs in mock_documents.items():
        if any(word in query_lower for word in key.split()):
            results.extend(docs)
    
    # Return top_k results
    if not results:
        results = ["No relevant documents found. Using general renewable energy information."]
    
    return results[:top_k]
