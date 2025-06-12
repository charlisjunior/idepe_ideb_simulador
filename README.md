# 📊 Simulador do IDEB/IDEPE

Este é um simulador interativo construído com [Streamlit](https://streamlit.io/) que permite calcular e visualizar o impacto das taxas de aprovação e das proficiências em Língua Portuguesa (LP) e Matemática (MT) no resultado do **IDEB** ou **IDEPE**, de acordo com a etapa de ensino.

## 🔧 Funcionalidades

- Escolha entre simular o **IDEB** ou o **IDEPE**
- Simulação para:
  - Anos Iniciais (1º ao 5º ano)
  - Anos Finais (6º ao 9º ano)
  - Ensino Médio
- Inserção manual das taxas de aprovação
- Inserção e ajuste das proficiências LP e MT
- Exibição dos cálculos:
  - Fluxo
  - Notas padronizadas LP e MT
  - Nota média (SAEPE/SAEB)
  - Resultado final do indicador
- Gráficos de simulação do impacto da variação da proficiência no resultado final

## 🚀 Como usar

### 1. Crie o ambiente virtual

```bash
python -m venv .venv
```

### 2. Ative o ambiente virtual

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode o simulador

```bash
streamlit run simulador_idepe_ideb.py
```

---

## 🧠 Observação

Este simulador foi desenvolvido com base nas fórmulas da planilha oficial de cálculo dos indicadores educacionais. Os resultados são estimativas e não substituem os cálculos realizados pelos sistemas oficiais.

## 📫 Contato

Charlis Cabral – [LinkedIn](https://linkedin.com/in/charliscabral)  
