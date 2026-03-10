import json
import logging
from datetime import datetime

# Desativa logs padrão do Python no terminal
logging.basicConfig(level=logging.INFO, format='%(message)s')

# arquivo externo com as logs
ARQUIVO_LOG = "classificador.log"

def log_estruturado(nivel, evento, detalhes):
    """Gera um log no formato JSON e anexa (append) no arquivo de log."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": nivel.upper(),
        "event": evento,
        "details": detalhes
    }
    
    # Dicionário para JSON
    json_string = json.dumps(log_entry, ensure_ascii=False)
    
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(json_string + "\n")

def parse_json_response(texto_resposta):
    """
    Tenta converter a string do LLM em um dicionário Python.
    Remove marcações de código Markdown (```json) se existirem.
    """
    try:
        texto_limpo = texto_resposta.strip()
        if texto_limpo.startswith("```json"):
            texto_limpo = texto_limpo[7:]
        if texto_limpo.endswith("```"):
            texto_limpo = texto_limpo[:-3]
            
        return json.loads(texto_limpo.strip())
    
    except Exception as e:
        log_estruturado("ERROR", "falha_parse_json", {"erro": str(e), "texto_cru": texto_resposta})
        return None

def validar_categoria(dados_json, categorias_permitidas):
    """
    Garante que a chave 'categoria' existe e que o valor não foi inventado pela IA.
    """
    if not isinstance(dados_json, dict) or "categoria" not in dados_json:
        log_estruturado("WARNING", "formato_invalido", {"dados": dados_json})
        return False
        
    categoria = dados_json.get("categoria")
    if categoria not in categorias_permitidas:
        log_estruturado("WARNING", "alucinacao_detectada", {"categoria_inventada": categoria})
        return False
        
    return True

def processar_resposta_com_fallback(texto_resposta, categorias_permitidas, fallback="Geral"):
    """
    Orquestra o fluxo: tenta processar, tenta validar e, se algo falhar, retorna o fallback.
    Também extrai o score de confiança gerado pelo modelo.
    """
    dados_json = parse_json_response(texto_resposta)
    
    # Se o JSON for válido e a categoria existir na lista
    if validar_categoria(dados_json, categorias_permitidas):
        # Captura o score de confiança. Se a IA esquecer de enviar, define como 0.0
        confianca = dados_json.get("confianca", 0.0)
        
        log_estruturado("INFO", "classificacao_sucesso", {
            "categoria": dados_json["categoria"],
            "confianca": confianca
        })
        
        # Retorna o dicionário completo com categoria e confiança
        return {"categoria": dados_json["categoria"], "confianca": confianca}
    
    # Se falhou no parse ou na validação, aciona o fallback
    log_estruturado("WARNING", "fallback_acionado", {"fallback": fallback})
    return {"categoria": fallback, "confianca": 0.0}