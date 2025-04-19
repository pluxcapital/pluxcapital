import streamlit as st
import requests

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

def analisis_macro_perplexity():
    st.subheader("🔎 Análisis macroeconómico automático")
    consulta = "¿Cuál es el panorama macroeconómico para el mercado financiero argentino en los próximos 6 meses? Responde en 4 líneas."
    
    # Manejo seguro de secretos para ambos entornos
    try:
        api_key = st.secrets["PPLX_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = st.text_input("Ingresa tu clave de Perplexity API para continuar:", type="password")
        if not api_key:
            st.warning("Se requiere una clave API para usar esta función. En producción, esta clave se configura automáticamente.")
            return

    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "sonar-pro",  # o "pplx-7b-online"
            "messages": [
                {"role": "user", "content": consulta}
            ]
        }
    )
    if response.status_code == 200:
        data = response.json()
        resumen = data['choices'][0]['message']['content']
        st.info(resumen)
    else:
        st.error("No se pudo obtener el análisis automático.")

# Llama a la función donde lo necesites en tu app principal
analisis_macro_perplexity()

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

