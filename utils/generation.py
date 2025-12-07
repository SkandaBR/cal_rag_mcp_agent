"""
Answer generation utility for RAG.
"""

def generate_answer(query: str, context: str, model: str = "default") -> str:
    """
    Generate an answer based on the query and retrieved context.
    
    Args:
        query: User's question
        context: Retrieved context from RAG
        model: Model to use for generation
        
    Returns:
        Generated answer string
    """
    # This is a placeholder - in production, this would call an LLM
    # For now, just return the context
    return f"Based on the query '{query}', here is the relevant information:\n\n{context}"
