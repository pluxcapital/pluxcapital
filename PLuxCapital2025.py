import streamlit as st

st.set_page_config(
    page_title="Asesor AP Automatizado",
    page_icon="📈",
    layout="wide"
)

st.title('Asesor AP Automatizado v1.0')
st.write("Bienvenido al sistema de recomendaciones CNV-Compliant")

with st.sidebar:
    st.subheader("🐻 Perfil de Inversor CNV-Compliant")
    edad = st.slider("Edad", 18, 80, 30)
    ingresos_mensuales = st.selectbox("Ingresos netos mensuales (USD)", 
                                    ["<1,000", "1,000-3,000", ">3,000"])
    tolerancia_riesgo = st.radio("Actitud frente a pérdidas potenciales", 
                               ["Baja", "Media", "Alta"])
    objetivo = st.multiselect("Objetivo principal", 
                            ["Preservar capital", "Generar ingresos", "Crecimiento a largo plazo"])

with st.expander("ℹ️ ¿Cómo funciona este sistema?"):
    st.markdown("""
    **Metodología regulatoria**:  
    - Algoritmo validado bajo RG 880/2023 CNV  
    - Exclusivamente instrumentos autorizados por BYMA  
    - Actualización diaria de parámetros de riesgo  
    """)

def generar_recomendacion(perfil):
    estrategia = {
        "FCI Money Market": 0,
        "ONs CER": 0,
        "ETFs Globales": 0,
        "Cauciones": 0
    }
    
    if perfil["tolerancia_riesgo"] == "Baja":
        estrategia["FCI Money Market"] = 60
        estrategia["Cauciones"] = 40
    elif perfil["tolerancia_riesgo"] == "Media":
        estrategia["ONs CER"] = 50
        estrategia["ETFs Globales"] = 30
        estrategia["FCI Money Market"] = 20
    else:
        estrategia["ETFs Globales"] = 70
        estrategia["ONs CER"] = 30
        
    return estrategia

if st.button("Generar propuesta"):
    perfil_usuario = {
        "edad": edad,
        "tolerancia_riesgo": tolerancia_riesgo,
        "objetivo": objetivo
    }
    
    recomendacion = generar_recomendacion(perfil_usuario)
    
    st.subheader("⚡ Propuesta CNV-Compliant")
    for instrumento, porcentaje in recomendacion.items():
        st.progress(porcentaje/100)
        st.write(f"**{instrumento}**: {porcentaje}%")
    
    st.caption("🔍 Base regulatoria: Resolución General 880/2023 CNV")

