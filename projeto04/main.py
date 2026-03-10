import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools import data_atual, calcular_imc, gerar_senha

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ARQUIVO_HISTORICO = "historico.json"

# --- CONFIGURAÇÃO DA PERSONA ---
MENSAGEM_SISTEMA = {
    "role": "system", 
    "content": (
        "Você é um assistente virtual objetivo. REGRAS OBRIGATÓRIAS:\n"
        "1. NUNCA invente dados. Se faltar peso/altura para o IMC ou o tamanho para a senha, PERGUNTE.\n"
        "2. Quando o usuário informar o dado que faltava (ex: responder apenas '10'), VOCÊ É OBRIGADO A EXECUTAR A FERRAMENTA 'gerar_senha'. Não responda apenas com texto.\n"
        "3. Quando a ferramenta te devolver o resultado, VOCÊ DEVE ESCREVER O DADO EXATO (a senha, o IMC ou a data) na sua mensagem para o usuário."
    )
}

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return [MENSAGEM_SISTEMA]

def salvar_historico():
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico_mensagens, f, indent=4, ensure_ascii=False)

historico_mensagens = carregar_historico()

def adicionar_mensagem(mensagem):
    historico_mensagens.append(mensagem)
    if len(historico_mensagens) > 11:
        historico_mensagens[:] = [historico_mensagens[0]] + historico_mensagens[-10:]
    salvar_historico()

tools = [
    {
        "type": "function",
        "function": {
            "name": "data_atual",
            "description": "Obtém a data de hoje."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_imc",
            "description": "Calcula o IMC. SÓ USE se o usuário já forneceu peso e altura.",
            "parameters": {
                "type": "object",
                "properties": {
                    "peso": {"type": "number", "description": "Peso em kg"},
                    "altura": {"type": "number", "description": "Altura em metros"}
                },
                "required": ["peso", "altura"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gerar_senha",
            "description": "Gera uma senha segura. OBRIGATÓRIO: O usuário deve informar o tamanho primeiro.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tamanho": {"type": "integer", "description": "Tamanho da senha. Mínimo 6."}
                },
                "required": ["tamanho"]
            }
        }
    }
]

def executar_ferramenta(tool_call):
    nome_funcao = tool_call.function.name
    texto_argumentos = tool_call.function.arguments
    
    if not texto_argumentos or texto_argumentos.strip() == "null":
        texto_argumentos = "{}"
        
    argumentos = json.loads(texto_argumentos)
    if argumentos is None:
        argumentos = {}

    if nome_funcao == "data_atual":
        return data_atual()
    elif nome_funcao == "calcular_imc":
        return calcular_imc(argumentos.get("peso"), argumentos.get("altura"))
    elif nome_funcao == "gerar_senha":
        return gerar_senha(argumentos.get("tamanho", 12))
        
    return "Ferramenta não encontrada."

def chat(pergunta):
    adicionar_mensagem({"role": "user", "content": pergunta})

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=historico_mensagens,
        tools=tools,
        tool_choice="auto"
    )

    mensagem_resposta = resposta.choices[0].message
    conteudo_assistente = mensagem_resposta.content if mensagem_resposta.content else ""

    if mensagem_resposta.tool_calls:
        print("\n⚙️ [SISTEMA]: O assistente está acionando uma ferramenta...") 
        
        adicionar_mensagem({
            "role": "assistant", 
            "content": conteudo_assistente, 
            "tool_calls": [t.model_dump() for t in mensagem_resposta.tool_calls]
        })
        
        for tool_call in mensagem_resposta.tool_calls:
            resultado_funcao = executar_ferramenta(tool_call)
            
            # IMPRIME O RESULTADO DIRETO NA TELA PARA VOCÊ VER
            print(f"✅ [RESULTADO DO PYTHON]: {resultado_funcao}")
            
            adicionar_mensagem({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(resultado_funcao)
            })
            
        resposta_final = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=historico_mensagens
        )
        resposta_conteudo = resposta_final.choices[0].message.content
        adicionar_mensagem({"role": "assistant", "content": resposta_conteudo})
        return resposta_conteudo

    if conteudo_assistente:
        adicionar_mensagem({"role": "assistant", "content": conteudo_assistente})
        return conteudo_assistente

# --- LOOP PRINCIPAL ---
print("Assistente: Olá! Eu sou o seu Assistente Virtual. 🤖")
print("Você pode me pedir a data, calcular IMC ou gerar uma senha.")
print("Dica: Digite '/limpar' para reiniciar o histórico ou 'sair' para encerrar o chat.")

while True:
    pergunta = input("\nVocê: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Assistente: Encerrando o chat. Até mais!")
        break

    if pergunta.strip().lower() in ["/limpar", "limpar"]:
        historico_mensagens.clear()
        historico_mensagens.append(MENSAGEM_SISTEMA)
        salvar_historico()
        print("Assistente: Memória da conversa apagada. Sobre o que quer falar agora?")
        continue

    resposta_assistente = chat(pergunta)
    print("\nAssistente: ", resposta_assistente)