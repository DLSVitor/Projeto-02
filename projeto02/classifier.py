from llm_client import gerar_resposta
from validator import processar_resposta_com_fallback

CATEGORIAS = ["Suporte", "Vendas", "Financeiro", "Geral"]

def classificar_mensagem(mensagem, temperature=0.2):
    # Melhoramos o prompt para evitar a confusão entre Suporte e Financeiro
    prompt = f"""
        Você é um assistente de triagem de atendimento ao cliente.
        Sua tarefa é classificar a mensagem do cliente em EXATAMENTE UMA das seguintes categorias: {', '.join(CATEGORIAS)}.
        
        Regras importantes de classificação:
        - Se a mensagem falar sobre problemas técnicos, erros no sistema ou dúvidas de uso, classifique como "Suporte".
        - Se a mensagem envolver pagamentos, cancelamento de assinatura, faturas ou estorno, classifique OBRIGATORIAMENTE como "Financeiro", mesmo que o cliente cite um erro no sistema no meio da frase.
        - Se for interesse em comprar, classifique como "Vendas".
        - Se não se encaixar em nada acima, use "Geral".

        Retorne apenas um JSON válido no formato exato:
        {{
            "categoria": "nome_categoria"
        }}

        Mensagem: "{mensagem}"
    """
    
    # 1. Pega a resposta crua da IA
    resposta_crua = gerar_resposta(prompt, temperature)
    
    # 2. Passa pela nossa esteira de limpeza e validação
    categoria_final = processar_resposta_com_fallback(
        texto_resposta=resposta_crua, 
        categorias_permitidas=CATEGORIAS, 
        fallback="Geral"
    )
    
    return categoria_final