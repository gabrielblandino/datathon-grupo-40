# OWASP Top 10 for LLMs - Mapeamento e Mitigação
1. **LLM01 (Prompt Injection):** Mitigado pelo filtro `InputGuardrail` rodando REGEX restritivas (ex: "ignore all previous instructions").
2. **LLM02 (Insecure Output Handling):** Mitigado pelo `OutputGuardrail` validando PII e escapando HTML do Agente ReAct no frontend.
3. **LLM04 (Model Denial of Service):** Limitado ao cap de tokens (4096 caracteres input).
4. **LLM06 (Sensitive Info Disclosure):** Uso da lib Presidio bloqueando emissão de e-mails, cpfs e registros corporativos.
5. **LLM09 (Overreliance):** Feedback Champion-challenger estabelecido via "Human-in-the-loop" implementado. Retreino condicionado à supervisão de AUC.

*Testes do Red Team focaram em injetar juros (int_rate) negativos manipulados na base de query (SQL injection pelo RAG) e em Bypass de Persona, onde ambos falharam, comprovando eficácia do Guardrails.*