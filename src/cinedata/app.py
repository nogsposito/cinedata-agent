import sys
from pathlib import Path

import streamlit as st


SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_DIR))

st.set_page_config(
    page_title="CineData Analytics",
    page_icon="🎬",
)

try:
    from cinedata.agent import agent

except Exception as error:
    st.error(
        f"Não foi possível iniciar o agente: {error}"
    )
    st.stop()

st.title("CineData Analytics")

st.write(
    "Faça perguntas em linguagem natural sobre o catálogo de filmes."
)

question = st.text_input(
    "Pergunta",
    placeholder="Ex: Quais são os 5 filmes mais populares?",
)

if st.button("Consultar") and question.strip():
    with st.spinner("Analisando dados..."):
        try:
            result = agent.run_sync(question.strip())

            st.subheader("Resposta")
            st.write(result.output.answer)

            with st.expander("Ver SQL utilizado"):
                st.code(
                    result.output.sql,
                    language="sql",
                )

        except Exception as error:
            st.error(
                f"Erro ao processar consulta: {error}"
            )