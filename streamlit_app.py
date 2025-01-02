import streamlit as st
import pandas as pd
import duckdb
#from datetime import datetime
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

varTitulo = 'Elecciones Ipstuneg 2025'
varCedula = ''
varFicha = ''
cursor = duckdb.connect()
cursor.execute("""CREATE TABLE tmp AS SELECT * FROM read_csv('db/db.csv');""")


st.set_page_config(
    layout="wide",
    page_title=varTitulo,
    page_icon=":white_check_mark:",
    initial_sidebar_state="collapsed",
    menu_items=None
)

#@st.cache_data
#def load_data():
#    #df = pd.read_csv('db/db.csv', sep=";")
#    cursor = duckdb.connect()
#    cursor.execute("""CREATE TABLE tmp AS SELECT * FROM read_csv('db/db.csv');""")
#    st.session_state["authenticated"] = False
#    st.session_state["username"] = ''
#    return cursor
def get_remote_ip() -> str:
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None
    
    return session_info.request.remote_ip

def getData():
    with st.form(varTitulo):
        varCedula = st.text_input("Cédula", placeholder="Ingrese su Cédula", max_chars=9)
        #varDataNacimiento = st.date_input("Fecha de Nacimiento", min_value=datetime(1934,1,1))
        varFicha = st.text_input("N Ficha", placeholder="Ingresu su número de ficha", max_chars=5)
        varEnviado = st.form_submit_button("Ingresar")

    return varEnviado

def votar():
    st.success(f'Puede iniciar su proceso de elección {st.session_state["username"]}')
    


def check_password():
    """Returns True if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Elector"):
            st.text_input("Cédula", placeholder="Ingrese su Cédula", max_chars=9, key="username")
            st.text_input("N Ficha", placeholder="Ingresu su número de ficha", max_chars=5, type="password", key="password")
            st.form_submit_button("Ingresar", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
       
        if st.session_state["username"] != "" and st.session_state["password"] != "":            
        
            df = cursor.execute(f"SELECT * FROM tmp WHERE CEDULA='{st.session_state['username'].upper()}' AND FICHA='{st.session_state['password']}';").df()

            if len(df) > 0:                
                st.session_state["username"] = str(df['NOMBRE'].iloc[0])
                st.session_state["password_correct"] = True                
                #del st.session_state["password"]  # Don't store the username or password.
                #del st.session_state["username"]         
            else:
                st.session_state["password_correct"] = False
        else:
            st.session_state["empty_values"] = True
            
    
    if st.session_state.get("password_correct", False):
        return True
    
    
    
    login_form()
    if "empty_values" in st.session_state:
        st.warning("Debe Ingresar su Cédula y su Ficha!")
        del  st.session_state["empty_values"]

    if "password_correct" in st.session_state:
        st.error("😕 Cédula o Número de Ficha incorrectos")
    return False

def main():
    st.title(varTitulo)
    st.write(get_remote_ip())

    if not check_password():
        st.stop()
    else:
        votar()
    

if __name__ == '__main__':
    main()
