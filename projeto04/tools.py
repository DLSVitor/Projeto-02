# tools.py
import datetime
import random
import string

def data_atual():
    """Retorna a data atual no formato YYYY-MM-DD."""
    return str(datetime.date.today())

def calcular_imc(peso, altura):
    """Calcula o Índice de Massa Corporal (IMC)."""
    try:
        imc = float(peso) / (float(altura) ** 2)
        return f"Seu IMC é {imc:.2f}"
    except Exception as e:
        return "Erro ao calcular o IMC. Verifique os valores de peso e altura."

def gerar_senha(tamanho=12):
    """Gera uma senha aleatória segura."""
    try:
        tamanho = int(tamanho)
        caracteres = string.ascii_letters + string.digits + "!@#$%&*()"
        senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
        return f"Sua senha gerada é: {senha}"
    except ValueError:
        return "Tamanho inválido para a senha."