# RastreIa - Data Lineage com Inteligência Artificial

O **RastreIa** é uma solução gratuita e open-source projetada para simplificar a rastreabilidade e o monitoramento do fluxo de dados entre etapas ou sistemas diferentes usando Inteligência Artificial (IA).

Com ele, usuários sem conhecimentos técnicos avançados podem facilmente identificar quando, onde e por que alterações ocorrem em seus dados.

## 🚀 Principais funcionalidades

- **Configuração Fácil:** Basta apontar o local dos seus dados (arquivos CSV, JSON, Parquet ou bancos locais).
- **IA automática:** Usa LLM local (Ollama) para interpretar mudanças e transformações nos dados.
- **Interface Simples:** Visualização intuitiva dos resultados, permitindo interação via chat para resolver dúvidas pontuais.

## Exemplos práticos de uso:

- Descubra exatamente em qual etapa um dado específico desapareceu ou foi alterado.
- Automatize auditorias internas ou compliance em pipelines de dados.
- Reduza significativamente o tempo gasto na investigação de problemas em fluxos de dados.

## 🚀 Como rodar localmente

### Requisitos
- Python 3.10+
- FastAPI
- Streamlit
- DuckDB
- Ollama (gratuito/local)

### Instalação
```bash
uv venv create rastre-ia-env
source rastre-ia-env/bin/activate
uv pip install fastapi duckdb streamlit pandas ollama
```

### Executar aplicação

**Backend:**
```bash
uvicorn backend.main:app --reload
```

**Frontend:**
```bash
streamlit run frontend/app.py
```

### Uso
Abra o navegador em `http://localhost:8501` e informe o caminho para sua pasta de dados ou banco de dados local.

## 💻 Stack Técnica
- **Backend:** FastAPI
- **Banco local:** DuckDB
- **IA:** Ollama (LLM gratuito rodando localmente)
- **Interface:** Streamlit

## 📝 Licença
Este projeto é gratuito, aberto e distribuído sob a licença MIT.

