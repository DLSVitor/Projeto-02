import json

def validate_json(response_text):
    try:
        # Tenta encontrar o início e o fim do JSON caso o modelo tenha colocado texto em volta
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end != -1:
            response_text = response_text[start:end]
            
        data = json.loads(response_text)
        if "status" not in data:
            raise ValueError("Campo 'status' obrigatório")
        return True, data
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")

# --- NOVA FUNÇÃO DE SEGURANÇA ---
def is_prompt_injection(query):
    """
    Verifica se a pergunta contém padrões comuns de ataque de Prompt Injection.
    """
    # Lista de termos suspeitos em minúsculo
    termos_proibidos = [
        "system prompt",
        "ignore as instruções",
        "ignore as regras",
        "esqueça tudo",
        "instruções anteriores",
        "modo desenvolvedor",
        "regras anteriores",
        "qual o seu prompt"
    ]
    
    query_lower = query.lower()
    
    for termo in termos_proibidos:
        if termo in query_lower:
            return True # Injeção detectada!
            
    return False # Segue o jogo, a pergunta parece segura.