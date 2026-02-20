from classifier import classificar_mensagem
import time
from collections import Counter

def rodar_testes_producao():
    # Escolhemos uma mensagem que mistura assuntos para ver como o modelo se sai
    mensagem_teste = "O sistema travou na hora do pagamento e agora quero cancelar minha assinatura."
    
    # As 3 temperaturas exigidas no desafio
    temperaturas = [0.0, 0.5, 1.0]
    repeticoes = 10
    
    relatorio = {}

    print("="*50)
    print("INICIANDO BATERIA DE TESTES DE PRODUÇÃO")
    print(f"Mensagem alvo: '{mensagem_teste}'")
    print("="*50)

    for temp in temperaturas:
        print(f"\n[!] Testando com Temperatura: {temp}")
        resultados_desta_temp = []
        
        for i in range(repeticoes):
            print(f"  -> Execução {i+1}/{repeticoes}...", end=" ", flush=True)
            
            # Chama a função que passa pela nossa esteira de validação
            resultado = classificar_mensagem(mensagem_teste, temperature=temp)
            resultados_desta_temp.append(resultado)
            
            print(f"Classificado como: {resultado}")
            
            # Pausa de 1 segundo entre as chamadas para evitar bloqueio da API (Rate Limit)
            time.sleep(1)
            
        relatorio[temp] = resultados_desta_temp

    # Imprime o resumo final para te ajudar a escrever o relatório da entrega
    print("\n" + "="*50)
    print("RESUMO PARA O RELATÓRIO COMPARATIVO")
    print("="*50)
    for temp, resultados in relatorio.items():
        contagem = Counter(resultados)
        print(f"Temperatura {temp}:")
        for categoria, qtd in contagem.items():
            print(f"  - {categoria}: {qtd} vez(es) ({qtd/repeticoes*100}%)")

if __name__ == "__main__":
    rodar_testes_producao()