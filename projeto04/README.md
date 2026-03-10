# Assistente Virtual com Memória e Ferramentas (Groq & Llama 3)

Projeto desenvolvido para o DESAFIO AULA 04. Trata-se de um chatbot inteligente que possui limite de histórico, persistência em arquivo, personalidade customizada e capacidades aumentadas via execução de funções Python (Tool Calling). 

O projeto foi migrado para utilizar o modelo open-source **Llama 3.3 70B** através da API ultrarrápida do **Groq**.

## 🚀 Funcionalidades Implementadas

- **Comando de Limpeza**: Digitar `/limpar` (ou apenas `limpar`) zera o histórico de conversas do arquivo e da memória.
- **Persona Rigorosa via System Prompt**: Comportamento configurado para ser prestativo, com regras estritas para evitar "alucinação de parâmetros" (o bot é obrigado a perguntar os dados que faltam antes de executar funções).
- **Limite de Histórico**: Gerenciamento de tokens eficaz, mantendo apenas a regra do sistema + as últimas 10 interações.
- **Persistência de Dados**: Todo o histórico é salvo automaticamente no arquivo `historico.json` e recarregado quando a aplicação reinicia.
- **Uso Autônomo de Funções (Tool Calling)**:
  - `data_atual()`: Retorna a data do dia.
  - `calcular_imc(peso, altura)`: Realiza cálculo matemático seguro via Python.
  - `gerar_senha(tamanho)`: Cria senhas aleatórias robustas com validação de tamanho mínimo (6 caracteres).
- **Logs Visuais de Execução**: Indicadores no terminal (`⚙️ [SISTEMA]` e `✅ [RESULTADO DO PYTHON]`) que mostram exatamente quando a IA decidiu acionar um script local e o que o script devolveu.

## 💻 Como Executar

1. Certifique-se de que o Python 3 está instalado.
2. Instale as dependências executando: `pip install -r requirements.txt`
3. Crie um arquivo `.env` na raiz do projeto e insira sua chave gratuita do Groq: `GROQ_API_KEY=gsk_suachaveaqui`
4. Execute a aplicação: `python main.py`

---

## 🚧 Dificuldades Encontradas no Desenvolvimento

Durante a construção deste assistente, enfrentei alguns desafios técnicos reais que exigiram adaptações no código:

1. **Limite de Cota na API:** O projeto original usava a OpenAI, mas esbarrei no erro `429 - insufficient_quota`. A solução foi migrar rapidamente a base de código para usar a API do **Groq** com o modelo *Llama 3*, mantendo a mesma estrutura de *Tool Calling*.
2. **Alucinação de Parâmetros:** Inicialmente, se o usuário pedisse para "calcular IMC" sem passar os dados, a IA inventava um peso e altura genéricos para entregar um resultado logo. Foi necessário criar um *System Prompt* muito rigoroso proibindo essa ação e forçando a IA a fazer perguntas ao usuário.
3. **Conflito de Persistência:** Ao atualizar as regras do *System Prompt* no código, a IA continuava ignorando as novas ordens. Descobri que isso ocorria porque o arquivo `historico.json` estava carregando a regra antiga salva nas execuções anteriores. A solução foi implementar o comando `/limpar` para zerar a memória e o arquivo.
4. **Omissão do Retorno da Ferramenta:** Em alguns testes, a IA executava a função de gerar senha com sucesso, mas decidia não mostrar a senha na resposta de texto (guardando a informação só para ela). Para contornar essa falha de comunicação, adicionei a regra `required` no mapeamento das ferramentas e criei prints nativos em Python (`✅ [RESULTADO DO PYTHON]`) para forçar a exibição do dado no terminal.

---

## 🧠 Reflexões sobre IA (Desafio Aula 04)

### 1. Se o histórico crescer muito, quais problemas podem ocorrer no uso de LLMs?
* **Custos Elevados/Esgotamento de Quota:** APIs cobram (ou limitam) por token. Enviar um histórico gigante a cada nova mensagem consome os limites rapidamente.
* **Estouro da Janela de Contexto:** Se o limite máximo de tokens do modelo for ultrapassado, a aplicação quebra.
* **Perda de Foco (Lost in the Middle):** O LLM perde a capacidade de raciocínio preciso quando há um mar de texto irrelevante ou muito antigo