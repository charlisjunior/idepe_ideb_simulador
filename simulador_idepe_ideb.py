import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador IDEB/IDEPE", layout="centered")
st.title("📊 Simulador do IDEB/IDEPE")

st.markdown("""
Este simulador calcula o valor estimado do IDEB ou IDEPE a partir das taxas de aprovação (1º ao 5º ano, 6º ao 9º ano ou Ensino Médio) e proficiências em LP e MT.
Você pode ajustar os valores e observar como isso afeta o resultado!
""")

# Escolha do indicador e etapa
indicador = st.selectbox("🔍 Qual indicador deseja simular?", ["IDEB", "IDEPE"])
etapa = st.selectbox("📚 Etapa de Ensino", ["Anos Iniciais (1º ao 5º ano)", "Anos Finais (6º ao 9º ano)", "Ensino Médio"])

st.header("🔢 Entradas de Dados")

# Aprovações
col1, col2, col3 = st.columns(3)
with col1:
    ap1 = st.number_input("Aprovação 1º Ano (%)", min_value=0.0, max_value=100.0, value=None, placeholder="")
    ap4 = st.number_input("Aprovação 4º Ano (%)", min_value=0.0, max_value=100.0, value=None, placeholder="")
with col2:
    ap2 = st.number_input("Aprovação 2º Ano (%)", min_value=0.0, max_value=100.0, value=None, placeholder="")
    ap5 = st.number_input("Aprovação 5º Ano (%)", min_value=0.0, max_value=100.0, value=None, placeholder="")
with col3:
    ap3 = st.number_input("Aprovação 3º Ano (%)", min_value=0.0, max_value=100.0, value=None, placeholder="")

# Proficiências e controles
st.markdown("---")
st.subheader("📘 Proficiência")
col_lp, col_mt = st.columns([1, 1])

with col_lp:
    prof_lp = st.number_input("Proficiência LP", min_value=0.0, max_value=1000.0, value=None, placeholder="")
    lp_change = st.number_input("⬆️⬇️ Ajuste LP (+/-)", step=5, value=0)
with col_mt:
    prof_mt = st.number_input("Proficiência MT", min_value=0.0, max_value=1000.0, value=None, placeholder="")
    mt_change = st.number_input("⬆️⬇️ Ajuste MT (+/-)", step=5, value=0)

if prof_lp is not None:
    prof_lp += lp_change
if prof_mt is not None:
    prof_mt += mt_change

# Cálculo do fluxo/rendimento
aprovacoes = [ap1, ap2, ap3, ap4, ap5]
aprovacoes_validas = [a for a in aprovacoes if a is not None and a > 0]
fluxo = np.prod(np.array(aprovacoes_validas) / 100) ** (1 / len(aprovacoes_validas)) if len(aprovacoes_validas) > 0 else 0
rendimento = fluxo

# Verificar se pode calcular o restante
if prof_lp is not None and prof_mt is not None:
    # Fórmulas de padronização
    if etapa == "Anos Iniciais (1º ao 5º ano)":
        nota_lp = ((prof_lp - 49) / 275) * 10
        nota_mt = ((prof_mt - 60) / 262) * 10
    elif etapa == "Anos Finais (6º ao 9º ano)":
        nota_lp = ((prof_lp - 100) / 300) * 10
        nota_mt = ((prof_mt - 100) / 300) * 10
    else:  # Ensino Médio
        nota_lp = ((prof_lp - 117) / 334) * 10
        nota_mt = ((prof_mt - 111) / 356) * 10

    # Garantir que nota mínima seja 0
    nota_lp = max(0, nota_lp)
    nota_mt = max(0, nota_mt)
    nota_saepe = (nota_lp + nota_mt) / 2

    # Resultado final
    resultado = nota_saepe * rendimento
    resultado_formatado = f"{resultado:.2f}" if indicador == "IDEPE" else f"{resultado:.1f}"

    st.markdown("---")
    st.header(f"📈 Resultado do {indicador}")
    st.metric("Fluxo (P)", f"{rendimento:.3f}")
    st.metric("Nota LP Padronizada", f"{nota_lp:.2f}")
    st.metric("Nota MT Padronizada", f"{nota_mt:.2f}")
    st.metric("Nota SAEPE / SAEB", f"{nota_saepe:.2f}")
    st.metric(f"{indicador} Estimado", resultado_formatado)

    # Gráfico
    st.markdown("---")
    st.subheader("📊 Impacto das Mudanças na Proficiência")

    x = np.arange(-20, 25, 5)

    if etapa == "Anos Iniciais (1º ao 5º ano)":
        notas_lp = [max(0, ((prof_lp + dx - 49)/275)*10) for dx in x]
        notas_mt = [max(0, ((prof_mt + dx - 60)/262)*10) for dx in x]
    elif etapa == "Anos Finais (6º ao 9º ano)":
        notas_lp = [max(0, ((prof_lp + dx - 100)/300)*10) for dx in x]
        notas_mt = [max(0, ((prof_mt + dx - 100)/300)*10) for dx in x]
    else:
        notas_lp = [max(0, ((prof_lp + dx - 117)/334)*10) for dx in x]
        notas_mt = [max(0, ((prof_mt + dx - 111)/356)*10) for dx in x]

    idebs_lp = [rendimento * ((n + nota_mt)/2) for n in notas_lp]
    idebs_mt = [rendimento * ((nota_lp + n)/2) for n in notas_mt]

    fig, ax = plt.subplots()
    ax.plot(x, idebs_lp, label='Variação LP', marker='o')
    ax.plot(x, idebs_mt, label='Variação MT', marker='s')
    ax.set_xlabel('Variação de Proficiência (± pontos)')
    ax.set_ylabel(f'{indicador} Estimado')
    ax.set_title('Impacto na Nota IDEB/IDEPE')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

st.markdown("""
💡 *Este simulador é uma estimativa baseada nas fórmulas da planilha. Valores reais podem variar conforme o modelo oficial.*
""")
