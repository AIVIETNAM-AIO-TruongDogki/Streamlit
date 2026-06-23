import streamlit as st
from statistic import Statistic



st.title("Student Grade Statistical Analysis !")
st.write("This is a simple application, which can upload a excel and make a statistic.")

# Upload excel file only (type -> excel)
file = st.file_uploader("Please upload your class's grade here!", type=["xlsx", "xls"])

if file is not None:
    sample_data = Statistic(file)
    st.dataframe(sample_data.show_data())
else:
    st.info("Please upload an Excel file.")


# Spinning when enter a query 
with st.form("Query_form"):
    query = st.text_input("Enter your query!")
    submmitted = st.form_submit_button("Submit")

if submmitted and query:
    with st.spinner("Processing..."):
        # when the spinning termintae -> result will be free -> can't assign
        # result = st.dataframe(sample_data.show_data()) 
        # st.dataframe(sample_data.process_query(query))
        result = sample_data.process_query(query)
        st.write(result)

