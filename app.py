import streamlit as st

import src.pipeline as pp
from src.statistic import Statistic

st.set_page_config(page_title="NLP Pipeline Demo", layout="centered")
st.title("Streamlit NLP Pipeline Demo")
st.caption("Translation + Spell Checking")

tab_t, tab_s, tab_ss = st.tabs(["Translation", "Spell Checking", "Grade Statistic"])


# ===== Tab 1: Translation =====
with tab_t:
    st.session_state.setdefault("res_t", None)

    with st.expander("Examples"):
        for example in pp.EXAMPLES_T:
            st.markdown(f"- {example}")

    with st.form("form_translate"):
        text_t = st.text_area(
            "Text to translate",
            height=90,
            placeholder="Enter your text...",
        )
        target = st.selectbox(
            "Translate to",
            list(pp.TARGET_LANGS.keys()),
        )
        submitted_t = st.form_submit_button("Translate", type="primary")

    if submitted_t:
        st.session_state.res_t = pp.run_translation(
            text_t,
            pp.TARGET_LANGS[target],
        )

    result_t = st.session_state.res_t
    if result_t:
        if result_t["ok"]:
            st.caption(
                f"Source: {result_t['source']} → Target: {result_t['target']}"
            )
            st.write(result_t["translated"])
            if result_t.get("note"):
                st.info(result_t["note"])
        else:
            st.warning(result_t["error"])


# ===== Tab 2: Spell checking =====
with tab_s:
    st.session_state.setdefault("res_s", None)

    with st.expander("Examples"):
        for example in pp.EXAMPLES_S:
            st.markdown(f"- {example}")

    st.caption(f"Supported languages: {', '.join(sorted(pp.SPELL_LANGS))}")

    with st.form("form_spell"):
        text_s = st.text_area(
            "Text to check",
            height=90,
            placeholder="Enter text to check its spelling...",
        )
        submitted_s = st.form_submit_button("Check spelling", type="primary")

    if submitted_s:
        st.session_state.res_s = pp.run_spellcheck(text_s)

    result_s = st.session_state.res_s
    if result_s:
        if result_s["ok"]:
            st.caption(f"Language: {result_s['language']}")
            st.write(result_s["fixed"])
            st.caption(
                "Spelling corrections applied"
                if result_s["changed"]
                else "No spelling errors detected"
            )
        else:
            st.warning(result_s["error"])

with tab_ss:
    st.session_state.setdefault("res_ss", None)

    st.write("This is a demo grade analysis application")
    file = st.file_uploader("Upload excel file", type=["xlsx", "xls"])

    if file is None:
        st.info("Upload an Excel file to begin.")
    else:
        example = Statistic(file)
        st.dataframe(example.show_data(), use_container_width=True)

        with st.form("form_statistic"):
            text_ss = st.text_area(
                "Enter the query",
                height=90,
                placeholder="Ready to query...",
            )
            submitted_ss = st.form_submit_button("Start", type="primary")

        if submitted_ss:
            st.session_state.res_ss = example.process_query(text_ss)

        if st.session_state.res_ss is not None:
            st.dataframe(st.session_state.res_ss, use_container_width=True)
