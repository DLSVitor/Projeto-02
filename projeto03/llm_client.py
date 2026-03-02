import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

# biblioteca gratuita para rodar os embeddings localmente
from sentence_transformers import SentenceTransformer

load_dotenv(override=True)


class LLMClient:
    def __init__(self, provider="openai"):
        self.provider = provider
        
        # --- PARTE PAGA (OpenAI Embeddings) COMENTADA ---
        # self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # --- PARTE GRATUITA (Local Embeddings) ---
        # Inicializa o modelo local.(cerca de 80mb)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        elif provider == "groq":
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
    def generate_text(self, system_prompt, user_prompt, temperature=0.2):

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        
        elif self.provider == "groq":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        
        # --- PARTE PAGA (OpenAI Embeddings) COMENTADA ---
        # response = self.openai_client.embeddings.create(
        #     input=[text], 
        #     model="text-embedding-3-small"
        # )
        # return response.data[0].embedding
        
        # --- PARTE GRATUITA (Local Embeddings) ---
        # Gera o vetor matematicamente usando a CPU/GPU do seu computador
        # e converte (.tolist()) para o mesmo formato que a OpenAI retornaria
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()