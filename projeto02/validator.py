import json
import logging

# Configuração simples de log para visualizar quando o fallback entra em ação
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

def parse_json_response(texto_resposta):

    try:
        # LLMs costumam retornar o JSON dentro de blocos de código Markdown
        texto_limpo = texto_resposta.strip()
        if texto_limpo.startswith("```json"):
            texto_limpo = texto_limpo[7:]
        if texto_limpo.endswith("```"):
            texto_limpo = texto_limpo[:-3]
            
        return json.loads(texto_limpo.strip())
    
    except json.JSONDecodeError as e:
        logging.error(f"Falha ao realizar o parse do JSON: {e}. Texto original: '{texto_resposta}'")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado no parser: {e}")
        return None

def validar_categoria(dados_json, categorias_permitidas):

    if not isinstance(dados_json, dict) or "categoria" not in dados_json:
        logging.warning("Formato JSON incorreto ou chave 'categoria' ausente.")
        return False
        
    categoria = dados_json.get("categoria")
    if categoria not in categorias_permitidas:
        logging.warning(f"Alucinação detectada! A categoria '{categoria}' não está na lista permitida.")
        return False
        
    return True

def processar_resposta_com_fallback(texto_resposta, categorias_permitidas, fallback="Geral"):

    dados_json = parse_json_response(texto_resposta)
    
    # Se o JSON for válido e a categoria existir na lista
    if validar_categoria(dados_json, categorias_permitidas):
        return dados_json["categoria"]
    
    # Se falhou no parse ou na validação, aciona o fallback
    logging.warning(f"Acionando fallback seguro. Retornando categoria: '{fallback}'")
    return fallback