import os
import openai
from dotenv import load_dotenv
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str, model="text-embedding-ada-002"):
    result = openai.Embedding.create(input=[text], model=model)
    return result['data'][0]['embedding']

def semantic_search(query: str, documents: List[str], top_k: int = 3):
    query_embedding = np.array(get_embedding(query)).reshape(1, -1)
    doc_embeddings = [get_embedding(doc) for doc in documents]
    similarities = cosine_similarity(query_embedding, np.array(doc_embeddings))
    top_indices = similarities[0].argsort()[-top_k:][::-1]
    return [documents[i] for i in top_indices]

async def answer_from_notions(query: str, documents: List[str]):
    top_docs = semantic_search(query, documents)
    context = "\n\n".join(top_docs)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Use the following Notion data to answer the user's question.\n\n{context}"},
            {"role": "user", "content": query}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']
