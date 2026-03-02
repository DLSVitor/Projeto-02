import os
import numpy as np
import PyPDF2
import docx

def ler_pdf(caminho_arquivo):
    """Extrai texto de arquivos PDF."""
    texto = ""
    try:
        with open(caminho_arquivo, 'rb') as f:
            leitor = PyPDF2.PdfReader(f)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n\n"
    except Exception as e:
        print(f"Erro ao ler PDF {caminho_arquivo}: {e}")
    return texto

def ler_docx(caminho_arquivo):
    """Extrai texto de arquivos do Word (DOCX)."""
    texto = ""
    try:
        doc = docx.Document(caminho_arquivo)
        for paragrafo in doc.paragraphs:
            if paragrafo.text.strip():
                texto += paragrafo.text + "\n"
        texto += "\n\n" # Separação no final para o chunking
    except Exception as e:
        print(f"Erro ao ler DOCX {caminho_arquivo}: {e}")
    return texto

def load_conhecimento():
    """Lê todos os arquivos (.txt, .pdf, .docx) da pasta conhecimento."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_conhecimento = os.path.join(base_dir, "conhecimento")
    
    texto_completo = ""
    
    # Verifica se a pasta existe
    if not os.path.exists(pasta_conhecimento):
        print(f"Aviso: Pasta {pasta_conhecimento} não encontrada. Crie a pasta e adicione arquivos.")
        return texto_completo
        
    print(f"Lendo arquivos da pasta: {pasta_conhecimento}...")
    
    # Vasculha todos os arquivos dentro da pasta
    for nome_arquivo in os.listdir(pasta_conhecimento):
        caminho_arquivo = os.path.join(pasta_conhecimento, nome_arquivo)
        
        # Ignora pastas, foca só nos arquivos
        if os.path.isfile(caminho_arquivo):
            if nome_arquivo.endswith(".txt"):
                print(f" - Lendo TXT: {nome_arquivo}")
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    texto_completo += f.read() + "\n\n"
            elif nome_arquivo.endswith(".pdf"):
                print(f" - Lendo PDF: {nome_arquivo}")
                texto_completo += ler_pdf(caminho_arquivo)
            elif nome_arquivo.endswith(".docx"):
                print(f" - Lendo DOCX: {nome_arquivo}")
                texto_completo += ler_docx(caminho_arquivo)
            else:
                print(f" - Formato não suportado ignorado: {nome_arquivo}")
                
    return texto_completo

def build_vector_memory(conhecimento_text, llm_client):
    """Transforma o texto em chunks e gera os embeddings."""
    print("Iniciando a vetorização do conhecimento... (Isso pode levar alguns segundos)")
    
    sections = conhecimento_text.split("\n\n")
    memory = []
    
    for section in sections:
        section = section.strip()
        if section:
            # Como a extração de PDFs pode gerar chunks muito pequenos ou gigantes, 
            # um sistema avançado faria um tratamento aqui, mas o split simples resolve o desafio.
            emb = llm_client.get_embedding(section)
            memory.append({
                "text": section,
                "embedding": emb
            })
            
    print(f"Vetorização concluída! {len(memory)} fragmentos carregados em memória.")
    return memory

def cosine_similarity(v1, v2):
    """Calcula a similaridade de cosseno."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def vector_search(query, memory, llm_client, top_k=2):
    """Gera o vetor da pergunta e busca os trechos mais parecidos."""
    query_emb = llm_client.get_embedding(query)
    
    results = []
    for item in memory:
        sim = cosine_similarity(query_emb, item["embedding"])
        results.append({
            "text": item["text"],
            "score": sim
        })
        
    results.sort(key=lambda x: x["score"], reverse=True)
    best_chunks = [res["text"] for res in results[:top_k]]
    
    print(f"[DEBUG] Melhor similaridade encontrada: {results[0]['score']:.4f}")
    
    return "\n\n".join(best_chunks)