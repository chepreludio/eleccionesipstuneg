import streamlit as st
import pandas as pd
import duckdb
#from datetime import datetime

varTitulo = 'Elecciones Ipstuneg 2025'
varCedula = ''
varFicha = ''


st.set_page_config(
    layout="wide",
    page_title=varTitulo,    
)



#df = pd.read_csv('db/db.csv', sep=";")
cursor = duckdb.connect()
cursor.execute("""CREATE TABLE tmp AS SELECT * FROM read_csv('db/db.csv');""")
st.session_state["authenticated"] = False
st.session_state["username"] = ''

def getData():
    with st.form(varTitulo):
        varCedula = st.text_input("Cédula", placeholder="Ingrese su Cédula")
        #varDataNacimiento = st.date_input("Fecha de Nacimiento", min_value=datetime(1934,1,1))
        varFicha = st.text_input("N Ficha", placeholder="Ingresu su número de ficha")
        varEnviado = st.form_submit_button("Ingresar")

    return varEnviado

def votar():
    st.success(st.session_state["username"])
    
    #if varEnviado:
    #    #if varCedula == "" and varDataNacimiento == datetime.now().date():
    #    if varCedula == "" and varFicha == "":
    #        st.warning("Debe Ingresar su Cédula y su Ficha!")
    #    else:
    #        #V09950668	07088
    #        df = cursor.execute(f"SELECT * FROM tmp WHERE CEDULA='{varCedula}' AND FICHA='{varFicha}';").fetchone()
    #        #st.success(f"{df}")
    #        if len(df) > 0:
    #            st.session_state["authenticated"] = True
    #            st.session_state["username"] = str(df[3])


def main():
    st.title("Elecciones Ipstuneg")    

    enviado = getData()
    st.write(enviado)
    
    if enviado:
        #if varCedula == "" and varDataNacimiento == datetime.now().date():
        st.write(f"{varCedula}")
        if varCedula == "" and varFicha == "":
            st.warning("Debe Ingresar su Cédula y su Ficha!")
        else:
            #V09950668	07088
            df = cursor.execute(f"SELECT * FROM tmp WHERE CEDULA='{varCedula}' AND FICHA='{varFicha}';").fetchone()
            #st.success(f"{df}")
            if len(df) > 0:
                st.session_state["authenticated"] = True
                st.session_state["username"] = str(df[3])
    else:
        st.write(enviado)
    #
    #if st.session_state["authenticated"]:
    #    if st.session_state["username"]:
    #        st.success(f"Welcome {st.session_state['username']}")
    #        ...
    #
    #    else:
    #        st.success("Welcome guest")
    #        ...
    #else:
    #    login()
    #    st.error("Not authenticated")

if __name__ == '__main__':
    main()
