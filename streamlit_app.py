import streamlit as st
import pandas as pd
import duckdb
#from datetime import datetime


#df = pd.read_csv('db/db.csv', sep=";")
cursor = duckdb.connect()
cursor.execute("""CREATE TABLE tmp AS SELECT * FROM read_csv('db/db.csv');""")

st.title("Elecciones Ipstuneg")
#st.dataframe(df, use_container_width=True)

with st.form("Elecciones Ipstuneg 2024"):
    varCedula = st.text_input("Cédula", placeholder="Ingrese su Cédula")
    #varDataNacimiento = st.date_input("Fecha de Nacimiento", min_value=datetime(1934,1,1))
    varFicha = st.text_input("N Ficha", placeholder="Ingresu su número de ficha")
    varEnviado = st.form_submit_button("Ingresar")

if varEnviado:
    #if varCedula == "" and varDataNacimiento == datetime.now().date():
    if varCedula == "" and varFicha == "":
        st.warning("Debe Ingresar su Cédula y su Ficha!")
    else:
        #V09950668	07088
        df = cursor.execute(f"SELECT * FROM tmp WHERE CEDULA='{varCedula}' AND FICHA='{varFicha}';").fetchone()
        st.success(f"{df}")

#if st.session_state["authenticated"]:
#    if st.session_state["username"]:
#        st.success(f"Welcome {st.session_state['username']}")
#        ...
#
#    else:
#        st.success("Welcome guest")
#        ...
#else:
#    st.error("Not authenticated")

