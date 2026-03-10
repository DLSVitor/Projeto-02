from llm_client import gerar_resposta
from validator import processar_resposta_com_fallback

CATEGORIAS = ["Suporte", "Vendas", "Financeiro", "Geral"]

def classificar_mensagem(mensagem, temperature=0.2):
    prompt = f"""
        Você é um assistente de triagem de atendimento ao cliente.
        Classifique a mensagem abaixo em EXATAMENTE UMA das seguintes categorias: {', '.join(CATEGORIAS)}.
        
        Regras importantes de classificação:
        - Problemas técnicos, erros no sistema ou dúvidas de uso: "Suporte".
        - Pagamentos, cancelamento, faturas ou estorno: "Financeiro".
        - Interesse em comprar ou orçamentos: "Vendas".
        - Se não se encaixar em nada acima: "Geral".

        Avalie também a sua confiança nessa classificação, atribuindo um valor de 0.0 a 1.0 (onde 1.0 é 100% de certeza).

        Retorne apenas um JSON válido no formato exato:
        {{
            "categoria": "nome_categoria",
            "confianca": 0.95
        }}

        Mensagem: "{mensagem}"
    """
    
    resposta_crua = gerar_resposta(prompt, temperature)
    
    resultado_final = processar_resposta_com_fallback(
        texto_resposta=resposta_crua, 
        categorias_permitidas=CATEGORIAS, 
        fallback="Geral"
    )
    
    return resultado_final