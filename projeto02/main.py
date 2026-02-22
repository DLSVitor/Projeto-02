from classifier import classificar_mensagem
import time
from collections import Counter

def testar_upgrades_opcionais():
    mensagens = [
        "O sistema travou na hora do pagamento e agora quero cancelar minha assinatura.",
        "Como faço para resetar minha senha? A tela fica toda branca.",
        "Gostaria de agendar uma demonstração do plano corporativo.",
        "Qual é o horário de atendimento de vocês aos sábados?",
        "Minha fatura veio cobrando um valor duplicado este mês!",
        "aksjdhaksjdhaksjd" 
    ]
    
    # Ferramentas para medir a distribuição
    distribuicao = Counter()
    confianca_total = 0.0
    total_processado = 0

    print("="*65)
    print("🚀 INICIANDO TESTE COM SCORE, LOG E DISTRIBUIÇÃO")
    print("="*65)

    for msg in mensagens:
        print(f"\n[Cliente]: '{msg}'")
        
        # O resultado agora é um dicionário: {"categoria": "...", "confianca": 0.9}
        resultado = classificar_mensagem(msg, temperature=0.2)
        
        categoria = resultado["categoria"]
        confianca = resultado["confianca"]
        
        # Atualizando métricas de distribuição
        distribuicao[categoria] += 1
        confianca_total += confianca
        total_processado += 1
        
        print(f" -> Categoria: {categoria} | Confiança: {confianca*100:.1f}%")
        time.sleep(1)

    # Imprimindo a métrica de distribuição de resultados
    print("\n" + "="*65)
    print("📊 MEDIÇÃO DA DISTRIBUIÇÃO DE RESULTADOS")
    print("="*65)
    
    for cat, qtd in distribuicao.items():
        percentual = (qtd / total_processado) * 100
        print(f"  - {cat}: {qtd} ocorrência(s) ({percentual:.1f}%)")
        
    media_confianca = (confianca_total / total_processado) * 100
    print(f"\n⭐ Confiança Média do Modelo nesta bateria: {media_confianca:.1f}%")

if __name__ == "__main__":
    testar_upgrades_opcionais()