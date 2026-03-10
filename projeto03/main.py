from llm_client import LLMClient
from retriever import load_conhecimento, build_vector_memory, vector_search
from validator import validate_json, is_prompt_injection
from prompt import build_system_prompt
from classifier import classificar_mensagem

def main():
    provider = input("Escolha o provedor (openai/groq): ").strip().lower()
    
    try:
        client = LLMClient(provider=provider)
    except ValueError as e:
        print(f"Erro: {e}")
        return

    print("\nCarregando base de conhecimento...")
    conhecimento_text = load_conhecimento()
    
    # Processa o texto e cria a memória vetorial (roda apenas uma vez na inicialização)
    memory = build_vector_memory(conhecimento_text, client)

    print("\nSistema pronto! Faça sua pergunta.")
    
    while True:
        query = input("\nDigite sua pergunta (ou 'sair' para encerrar): ").strip()
        if query.lower() == "sair":
            break
            
        if not query:
            continue
            
        triagem = classificar_mensagem(query)
        print(f"[Triagem]: Categoria → {triagem['categoria']} | Confiança → {triagem['confianca']*100:.1f}%")
        
        # --- CAMADA DE SEGURANÇA: Proteção contra Prompt Injection ---
        if is_prompt_injection(query):
            continue # Pula o resto do código e pede uma nova pergunta
        # 1. Busca os trechos mais relevantes usando matemática (similaridade de cosseno)
        contexto = vector_search(query, memory, client, top_k=6)
        
        # 2. Prepara os prompts
        system_prompt = build_system_prompt()
        user_prompt = f"Contexto recuperado da base de conhecimento:\n{contexto}\n\nPergunta do usuário: {query}"

        # 3. Gera a resposta
        response_text = client.generate_text(system_prompt, user_prompt)

        # 4. Valida e exibe o JSON
        try:
            is_valid, data = validate_json(response_text)
            if is_valid:
                # Se o status for 'não encontrado', podemos avisar de forma amigável
                if data.get("status") == "não encontrado":
                    print(f"\n[Aviso do Sistema]: {data['resposta']}")
                else:
                    print(f"\nResposta: {data['resposta']}")
        except ValueError as e:
            print(f"\nErro de validação: {e}\nResposta crua do modelo: {response_text}")

if __name__ == "__main__":
    main()