# ==============================================================================
#  SIMULADOR IDEB/IDEPE - VERSÃO FINAL COM BIBLIOTECA CORRIGIDA (fpdf2)
# ==============================================================================

# --- 0. IMPORTAÇÕES NECESSÁRIAS ---
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from fpdf import FPDF # O nome do import não muda

# --- 1. CONFIGURAÇÃO CENTRALIZADA ---
ETAPAS_CONFIG = {
    "Anos Iniciais (1º ao 5º ano)": {
        "anos": ["1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano"],
        "padronizacao": {"lp": (49, 275), "mt": (60, 262)}
    },
    "Anos Finais (6º ao 9º ano)": {
        "anos": ["6º Ano", "7º Ano", "8º Ano", "9º Ano"],
        "padronizacao": {"lp": (100, 300), "mt": (100, 300)}
    },
    "Ensino Médio": {
        "anos": ["1º Ano EM", "2º Ano EM", "3º Ano EM"],
        "padronizacao": {"lp": (117, 334), "mt": (111, 356)}
    }
}

# --- 2. FUNÇÕES DE LÓGICA E UTILIDADES ---

def limpar_campos():
    st.session_state.clear()

def calcular_fluxo(aprovacoes):
    aprovacoes_validas = [a for a in aprovacoes if a is not None]
    if not aprovacoes_validas: return 0.0
    taxas = np.array(aprovacoes_validas) / 100.0
    return np.prod(taxas) ** (1 / len(taxas))

def padronizar_nota(proficiencia, parametros):
    const_sub, const_div = parametros
    nota = ((proficiencia - const_sub) / const_div) * 10
    return max(0, nota)

def criar_grafico_simulacao(data):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data['x_range'], data['ideb_sim_lp'], 'o-', label="Variação LP")
    ax.plot(data['x_range'], data['ideb_sim_mt'], 's-', label="Variação MT")
    ax.set_xlabel('Variação de Proficiência (± pontos)')
    ax.set_ylabel(f"{data['indicador']} Estimado")
    ax.set_title(f"Simulação de Impacto no {data['indicador']}")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    return fig

def gerar_relatorio_pdf(resultados, fig):
    """Gera o PDF usando a abordagem em memória, que funciona com fpdf2."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Relatório do Simulador - {resultados['indicador']}", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Etapa: {resultados['etapa']}", ln=True, align="C")
    pdf.ln(10)
    for chave, valor in resultados['metricas'].items():
        pdf.cell(80, 10, str(chave), border=1)
        pdf.cell(0, 10, str(valor), border=1, ln=True)
    pdf.ln(10)

    # Abordagem em memória: a mais limpa e eficiente.
    with io.BytesIO() as image_buffer:
        fig.savefig(image_buffer, format="png", dpi=150)
        # Com a biblioteca fpdf2, esta chamada funciona corretamente.
        pdf.image(image_buffer, w=190)

    return bytes(pdf.output())

# --- 3. FLUXO PRINCIPAL DA APLICAÇÃO (main) ---

def main():
    st.title("📊 Simulador do IDEB/IDEPE")
    st.markdown("Selecione a etapa, preencha os campos e clique em 'Calcular'.")

    if st.button("🔄 Limpar todos os campos", on_click=limpar_campos):
        st.success("Campos reiniciados!")
        st.rerun()

    indicador = st.selectbox("🔍 Qual indicador deseja simular?", ["IDEB", "IDEPE"], key="indicador")
    etapa = st.selectbox("📚 Etapa de Ensino", list(ETAPAS_CONFIG.keys()), key="etapa")
    st.markdown("---")
    
    with st.form(key="simulation_form"):
        st.header("🔢 Entradas de Dados")
        st.subheader("Taxas de Aprovação (%)")
        config = ETAPAS_CONFIG[etapa]
        cols = st.columns(3)
        aprovacoes = []
        for i, ano in enumerate(config["anos"]):
            aprovacoes.append(cols[i % 3].number_input(
                f"Aprovação {ano}", key=f"ap_{i}", min_value=0.0, max_value=100.0, value=None
            ))

        st.subheader("📘 Proficiência")
        col_lp, col_mt = st.columns(2)
        prof_lp_base = col_lp.number_input("Proficiência LP", key="prof_lp", value=None)
        lp_change = col_lp.number_input("⬆️⬇️ Ajuste LP (+/-)", key="lp_change", step=5, value=0)
        prof_mt_base = col_mt.number_input("Proficiência MT", key="prof_mt", value=None)
        mt_change = col_mt.number_input("⬆️⬇️ Ajuste MT (+/-)", key="mt_change", step=5, value=0)

        submitted = st.form_submit_button("Calcular e Simular")

    if submitted:
        if prof_lp_base is None or prof_mt_base is None:
            st.error("Por favor, preencha as proficiências de LP e MT.")
        else:
            prof_lp = prof_lp_base + lp_change
            prof_mt = prof_mt_base + mt_change
            rendimento = calcular_fluxo(aprovacoes)
            params_lp = config["padronizacao"]["lp"]
            params_mt = config["padronizacao"]["mt"]
            nota_lp = padronizar_nota(prof_lp, params_lp)
            nota_mt = padronizar_nota(prof_mt, params_mt)
            nota_saepe = (nota_lp + nota_mt) / 2
            resultado = nota_saepe * rendimento
            resultado_formatado = f"{resultado:.1f}" if indicador == "IDEB" else f"{resultado:.2f}"

            metricas_resultados = {
                "Fluxo (P)": f"{rendimento:.3f}", "Nota LP Padronizada": f"{nota_lp:.2f}",
                "Nota MT Padronizada": f"{nota_mt:.2f}", "Nota SAEPE / SAEB": f"{nota_saepe:.2f}",
                f"{indicador} Estimado": resultado_formatado
            }
            st.markdown("---")
            st.header(f"📈 Resultado do {indicador}")
            for chave, valor in metricas_resultados.items():
                st.metric(chave, valor)
            
            x_range = np.arange(-20, 25, 5)
            sim_data = {
                'x_range': x_range, 'indicador': indicador,
                'ideb_sim_lp': [rendimento * ((padronizar_nota(prof_lp_base + dx, params_lp) + nota_mt) / 2) for dx in x_range],
                'ideb_sim_mt': [rendimento * ((nota_lp + padronizar_nota(prof_mt_base + dx, params_mt)) / 2) for dx in x_range]
            }
            fig = criar_grafico_simulacao(sim_data)
            st.pyplot(fig)

            pdf_data = gerar_relatorio_pdf({
                'indicador': indicador, 'etapa': etapa, 'metricas': metricas_resultados
            }, fig)
            nome_arquivo = f"Relatorio_{indicador}_{etapa.replace(' ', '_')}.pdf"
            st.download_button("📥 Baixar Relatório em PDF", data=pdf_data, file_name=nome_arquivo, mime="application/pdf")

    st.markdown("---")
    st.markdown("💡 *Este simulador é uma estimativa. Valores reais podem variar.*")

if __name__ == '__main__':
    main()