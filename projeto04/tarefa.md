# DESAFIO AULA 04 - Assistente com Memória

> Evoluir o chatbot desenvolvido em aula, adicionando funcionalidades que tornem a aplicação mais útil e robusta.

---

## O que deve ser feito

- [X] **Parte 1 - Controle de Memória** -> Implementar comando `/limpar` para apagar histórico
- [X] **Parte 1 - Controle de Memória** -> Assistente informa "Memória da conversa apagada."
- [X] **Parte 2 - Persona do Assistente** -> Adicionar mensagem de sistema definindo comportamento
- [X] **Parte 2 - Persona do Assistente** -> Respostas devem refletir a personalidade definida
- [ ] **Parte 3 - Limite de Memória** -> Implementar limite de histórico (máximo últimas 10 mensagens)
- [ ] **Parte 3 - Limite de Memória** -> Remover mensagens mais antigas quando limite ultrapassado
- [ ] **Parte 4 - Integração de Funções Python** -> Implementar pelo menos 2 funções (calcular idade, conversor de temperatura, gerador de senha, cálculo de IMC, etc)
- [ ] **Parte 4 - Integração de Funções Python** -> Usar correto da função quando a pergunta exigir
- [ ] **Parte 5 - Persistência de Dados** -> Salvar histórico em arquivo JSON
- [ ] **Parte 5 - Persistência de Dados** -> Carregar histórico ao reiniciar programa

---

## Dicas

- Use a persona para manter a coerência das respostas
- Implemente um gerenciador de memória para controlar o histórico
- Teste o comportamento com múltiplas conversas
- Mantenha o JSON em um formato legível
- Identifique quando a pergunta do usuário requer uma função específica e execute-a automaticamente

---

## Entrega

- código fonte
- pequeno README explicando como executar, funcionalidades implementadas, reflexões e dificuldades encontradas

---

## Reflexão

Inclua no README
- Se o histórico crescer muito, quais problemas podem ocorrer no uso de LLMs?
- Por que algumas tarefas são melhores resolvidas por funções Python do que pelo próprio LLM?
- Quais riscos existem ao deixar que o LLM tome decisões sobre quando usar uma função?
```