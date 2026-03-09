import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import joblib
import os
import json
from sklearn.preprocessing import StandardScaler
from streamlit_lottie import st_lottie

# =====================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="CardioPredict Pro | Sistema de Predicción Cardíaca",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FUNCIÓN PARA CARGAR ANIMACIÓN LOTTIE

def load_lottiefile(filepath: str):
    """Carga una animación Lottie desde un archivo JSON local."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# FUNCIONES PARA GESTIÓN DE HISTORIAL

HISTORIAL_FILE = "docs/historial_pacientes.csv"
os.makedirs("docs", exist_ok=True)

def cargar_historial():
    """Carga el historial de pacientes desde CSV"""
    if os.path.exists(HISTORIAL_FILE):
        try:
            return pd.read_csv(HISTORIAL_FILE)
        except:
            return pd.DataFrame(columns=[
                'Fecha', 'Hora', 'ID_Paciente', 'Edad', 'Sexo', 
                'FC_Maxima', 'Glucosa_Ayunas', 'Angina_Ejercicio',
                'Tipo_Dolor', 'Pendiente_ST', 
                'Probabilidad_%', 'Clasificacion', 'Riesgo'
            ])
    else:
        return pd.DataFrame(columns=[
            'Fecha', 'Hora', 'ID_Paciente', 'Edad', 'Sexo', 
            'FC_Maxima', 'Glucosa_Ayunas', 'Angina_Ejercicio',
            'Tipo_Dolor', 'Pendiente_ST', 
            'Probabilidad_%', 'Clasificacion', 'Riesgo'
        ])

def guardar_registro(patient_id, datos, probabilidad, clasificacion):
    """Guarda un nuevo registro de paciente en el historial"""
    from datetime import datetime
    
    # Cargar historial existente
    df_historial = cargar_historial()
    
    # Crear nuevo registro
    nuevo_registro = {
        'Fecha': datetime.now().strftime('%Y-%m-%d'),
        'Hora': datetime.now().strftime('%H:%M:%S'),
        'ID_Paciente': patient_id if patient_id else 'SIN-ID',
        'Edad': datos['age'],
        'Sexo': 'M' if datos['sex'] == 1 else 'F',
        'FC_Maxima': datos['max_hr'],
        'Glucosa_Ayunas': 'Sí' if datos['fasting_bs'] == 1 else 'No',
        'Angina_Ejercicio': datos['exercise_angina'],
        'Tipo_Dolor': datos['chest_pain_type'],
        'Pendiente_ST': datos['st_slope'],
        'Probabilidad_%': round(probabilidad, 2),
        'Clasificacion': clasificacion,
        'Riesgo': 'ALTO' if clasificacion == "Alto Riesgo" else 'BAJO'
    }
    
    # Añadir al historial
    df_historial = pd.concat([df_historial, pd.DataFrame([nuevo_registro])], ignore_index=True)
    
    # Guardar en CSV
    df_historial.to_csv(HISTORIAL_FILE, index=False)
    
    return True

def exportar_historial():
    """Retorna el DataFrame del historial para descarga"""
    return cargar_historial()


# ESTILOS CSS PERSONALIZADOS

st.markdown("""
<style>
    /* Importar fuente profesional */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Estilos generales */
    .main {
        background-color: #F5F5F5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Ocultar padding superior de Streamlit */
    .block-container {
         padding-top: 0.1rem;
    }
    
    /* Header personalizado */
    .custom-header {
        background: linear-gradient(135deg, #1A1A1A 0%, #2C2C2C 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    # .header-text h1 {
    #     color:#E63946;
    #     font-size: 2.5rem;
    #     font-weight: 700;
    #     margin: 0;
    # }
    
    .header-text p {
        color: #CCCCCC;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #E63946;
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        color: #1A1A1A;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        color: #E63946;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-card .value-text {
        color: #E63946;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    /* Panel de resultados */
    .risk-high {
        background: linear-gradient(135deg, #E63946 0%, #C92A35 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #06D6A0 0%, #05B389 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    
    .risk-high h2, .risk-low h2 {
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }
    
    .risk-high p, .risk-low p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Botón principal */
    .stButton > button {
        background: linear-gradient(135deg, #E63946 0%, #C92A35 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(230, 57, 70, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(230, 57, 70, 0.4);
    }
    
    /* Info boxes */
    .info-box {
        background: #FFF4E6;
        border-left: 4px solid #FF9500;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #FFE5E5;
        border-left: 4px solid #E63946;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666666;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    /* Eliminar espacios entre columnas en el header */
    [data-testid="column"]:has(iframe) {
        padding: 0 !important;
    }
    
    /* Hacer tabs más grandes */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
}

.stTabs [data-baseweb="tab"] {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    padding: 1rem 2rem !important;
}

.stTabs [data-baseweb="tab-list"] button {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

.stTabs [data-baseweb="tab-list"] button p {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}
/* Animación de latido para el corazón */
@keyframes heartbeat {
    0%, 100% { 
        transform: scale(1); 
    }
    10%, 30% { 
        transform: scale(1.1); 
    }
    20%, 40% { 
        transform: scale(1); 
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================

@st.cache_resource
def cargar_modelo():
    """
    Carga el modelo entrenado y el scaler.
    Busca en la carpeta 'models' los archivos .pkl
    """
    try:
        modelo = joblib.load('models/modelo_coronario.pkl')
        scaler = joblib.load('models/scaler_coronario.pkl')
        return modelo, scaler, True
    except FileNotFoundError:
        st.error("⚠️ No se encontraron los archivos del modelo. Asegúrate de tener la carpeta 'models' con los archivos 'modelo_coronario.pkl' y 'scaler_coronario.pkl'")
        return None, None, False

def preparar_datos_para_prediccion(datos, scaler):
    """
    Prepara los datos del paciente en el formato correcto para el modelo.
    """
    # Crear las columnas one-hot para ChestPainType
    cp_asy = 1 if datos['chest_pain_type'] == 'ASY' else 0
    cp_ata = 1 if datos['chest_pain_type'] == 'ATA' else 0
    cp_nap = 1 if datos['chest_pain_type'] == 'NAP' else 0
    cp_ta = 1 if datos['chest_pain_type'] == 'TA' else 0
    
    # Crear las columnas one-hot para ST_Slope
    st_slope_flat = 1 if datos['st_slope'] == 'Flat' else 0
    st_slope_up = 1 if datos['st_slope'] == 'Up' else 0
    st_slope_down = 1 if datos['st_slope'] == 'Down' else 0
    
    # ExerciseAngina convertido a binario
    exercise_angina_bin = 1 if datos['exercise_angina'] == "Sí" else 0
    
    # Crear DataFrame
    X = pd.DataFrame([[
        datos['age'], datos['sex'], datos['max_hr'], datos['fasting_bs'],
        exercise_angina_bin, cp_asy, cp_ata, cp_nap, cp_ta,
        st_slope_flat, st_slope_up, st_slope_down
    ]], columns=[
        'Age', 'Sex', 'MaxHR', 'FastingBS', 'ExerciseAngina',
        'CP_ASY', 'CP_ATA', 'CP_NAP', 'CP_TA',
        'ST_Slope_Flat', 'ST_Slope_Up', 'ST_Slope_Down'
    ])
    
    # Aplicar escalado SOLO a Age y MaxHR
    X_scaled = X.copy()
    cols_para_escalar = ['Age', 'MaxHR']
    X_scaled[cols_para_escalar] = scaler.transform(X[cols_para_escalar])
    
    return X_scaled

def predecir_riesgo(datos, modelo, scaler):
    """Realiza la predicción de riesgo cardíaco"""
    if modelo is None or scaler is None:
        return 0, "Sin modelo", [0, 0]
    
    X_preparado = preparar_datos_para_prediccion(datos, scaler)
    probabilidades = modelo.predict_proba(X_preparado)[0]
    probabilidad_enfermedad = probabilidades[1] * 100
    clasificacion = "Alto Riesgo" if probabilidad_enfermedad >= 40 else "Bajo Riesgo"
    
    return probabilidad_enfermedad, clasificacion, probabilidades

def crear_gauge_chart(probabilidad):
    """Crea un medidor visual del riesgo"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probabilidad,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Nivel de Riesgo (%)", 'font': {'size': 24, 'color': '#1A1A1A'}},
        delta={'reference': 40, 'increasing': {'color': "#E63946"}, 'decreasing': {'color': "#06D6A0"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#1A1A1A"},
            'bar': {'color': "#E63946" if probabilidad >= 40 else "#06D6A0"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E0E0E0",
            'steps': [
                {'range': [0, 40], 'color': '#E8F5E9'},
                {'range': [40, 70], 'color': '#FFF4E6'},
                {'range': [70, 100], 'color': '#FFE5E5'}
            ],
            'threshold': {
                'line': {'color': "#E63946", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "#1A1A1A", 'family': "Inter"},
        height=350
    )
    
    return fig

def crear_radar_chart(datos):
    """Crea un gráfico de radar con los factores de riesgo"""
    categorias = ['Edad', 'Frec. Cardíaca', 'Glucosa', 'Tipo Dolor', 'Angina', 'Pendiente ST']
    
    valores = [
        min((datos['age'] / 100) * 100, 100),
        min((datos['max_hr'] / 200) * 100, 100),
        datos['fasting_bs'] * 100,
        {'ASY': 100, 'TA': 75, 'ATA': 50, 'NAP': 25}[datos['chest_pain_type']],
        100 if datos['exercise_angina'] == "Sí" else 0,
        {'Flat': 100, 'Down': 75, 'Up': 25}[datos['st_slope']]
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        fillcolor='rgba(230, 57, 70, 0.3)',
        line=dict(color='#E63946', width=2),
        name='Factores del Paciente'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#E0E0E0'),
            bgcolor='white'
        ),
        showlegend=False,
        paper_bgcolor='white',
        font={'color': "#1A1A1A", 'family': "Inter"},
        height=400
    )
    
    return fig


# CARGAR MODELO Y ANIMACIÓN

modelo, scaler, modelo_cargado = cargar_modelo()
lottie_heart = load_lottiefile("./assets/Heart with ECG.json")

# HEADER CON ANIMACIÓN LOTTIE

# Crear contenedor centrado
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
</div>
""", unsafe_allow_html=True)

# Columnas para centrar el contenido
col_anim, col_text = st.columns([2, 3])

with col_anim:
    if lottie_heart:
        st_lottie(lottie_heart, height=350, key="header_heart", quality="high", speed=1)
    else:
        st.markdown("<div style='font-size: 12rem; text-align: center; line-height: 1;'>❤️</div>", unsafe_allow_html=True)

with col_text:
    st.markdown("""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 250px;">
        <h1 style="color: #DC143C; font-size: 4rem; font-weight: 700; margin: 0; line-height: 1.2;">
            CardioPredict Pro
        </h1>
        <p style="color: #666666; font-size: 1.2rem; margin-top: 1rem; margin-bottom: 0; line-height: 1.4;">
            Sistema Inteligente de Evaluación de Riesgo Cardiovascular
        </p>
    </div>
    """, unsafe_allow_html=True)


# VERIFICAR MODELO

if not modelo_cargado:
    st.warning("""
    ### 📁 Instrucciones para cargar el modelo:
    
    1. Crea una carpeta llamada `models` en el mismo directorio que esta aplicación
    2. Coloca los siguientes archivos dentro de la carpeta `models`:
       - `modelo_coronario.pkl` (tu modelo entrenado)
       - `scaler_coronario.pkl` (tu scaler entrenado)
    3. Coloca tu animación Lottie en `./assets/Heart with ECG.json`
    4. Recarga la aplicación
    """)
    st.stop()

# SIDEBAR - ENTRADA DE DATOS

with st.sidebar:
    
    # Header personalizado del sidebar
    with st.sidebar:
    # Header personalizado del sidebar - blanco con acento rojo
     st.markdown("""
      <div style="text-align: center; 
                padding: 1.5rem; 
                background: white; 
                border-radius: 15px; 
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 15px rgba(230, 57, 70, 0.2);
                border: 2px solid #E63946;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem; animation: heartbeat 1s infinite;">❤️</div>
        <h3 style="color: #1A1A1A; margin: 0; font-size: 1.3rem; font-weight: 700;">Datos del Paciente</h3>
        <div style="width: 60px; height: 3px; background: #E63946; margin: 0.8rem auto 0 auto; border-radius: 2px;"></div>
       </div>
       """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    st.title("Datos del Paciente")
    
    st.markdown("---")
    
    st.subheader("Información General")
    patient_id = st.text_input("ID del Paciente", placeholder="Ej: PAC-2026-01")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Edad", min_value=1, max_value=120, value=50, step=1)
    with col2:
        sex = st.selectbox("Sexo", ["Masculino", "Femenino"])
    
    st.markdown("---")
    st.subheader("Parámetros Cardíacos")
    
    max_hr = st.number_input(
        "Frecuencia Cardíaca Máxima (bpm)",
        min_value=60, max_value=220, value=150, step=1,
        help="Frecuencia cardíaca máxima alcanzada durante ejercicio"
    )
    
    fasting_bs = st.selectbox(
        "Glucosa en Ayunas > 120 mg/dl",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Sí",
        help="Indica si la glucosa en ayunas supera los 120 mg/dl"
    )
    
    st.markdown("---")
    st.subheader("Síntomas y ECG")
    
    exercise_angina = st.selectbox(
        "Angina Inducida por Ejercicio",
        ["No", "Sí"],
        help="Dolor torácico durante actividad física"
    )
    
    chest_pain_type = st.selectbox(
        "Tipo de Dolor Torácico",
        ["ASY", "ATA", "NAP", "TA"],
        format_func=lambda x: {
            "ASY": "Asintomático",
            "ATA": "Angina Atípica",
            "NAP": "Dolor No Anginoso",
            "TA": "Angina Típica"
        }[x],
        help="Tipo de dolor en el pecho reportado por el paciente"
    )
    
    st_slope = st.selectbox(
        "Pendiente del Segmento ST",
        ["Flat", "Up", "Down"],
        format_func=lambda x: {
            "Flat": "Plana",
            "Up": "Ascendente",
            "Down": "Descendente"
        }[x],
        help="Pendiente del segmento ST en el electrocardiograma de esfuerzo"
    )
    
    st.markdown("---")
    analizar = st.button("ANALIZAR RIESGO CARDÍACO", use_container_width=True)
    

# CONTENIDO PRINCIPAL

tab1, tab2, tab3 = st.tabs(["📊 Análisis de Riesgo", "📈 Visualizaciones", "ℹ️ Información Médica"])

with tab1:
    if analizar:
        datos_paciente = {
            'age': age,
            'sex': 1 if sex == "Masculino" else 0,
            'max_hr': max_hr,
            'fasting_bs': fasting_bs,
            'exercise_angina': exercise_angina,
            'chest_pain_type': chest_pain_type,
            'st_slope': st_slope
        }
        
        probabilidad, clasificacion, probs = predecir_riesgo(datos_paciente, modelo, scaler)
        # Guardar en el historial
        guardar_registro(patient_id, datos_paciente, probabilidad, clasificacion)
        
        if clasificacion == "Alto Riesgo":
            st.markdown(f"""
            <div class="risk-high">
                <h2>⚠️ ALTO RIESGO DETECTADO</h2>
                <p>Probabilidad de enfermedad cardíaca: {probabilidad:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="risk-low">
                <h2>✓ RIESGO BAJO</h2>
                <p>Probabilidad de enfermedad cardíaca: {probabilidad:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📅 Edad</h3>
                <div class="value">{age}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>❤️ FC Máxima</h3>
                <div class="value">{max_hr}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            dolor_texto = {
                "ASY": "Asintomático",
                "ATA": "Ang. Atípica",
                "NAP": "No Anginoso",
                "TA": "Ang. Típica"
            }[chest_pain_type]
            st.markdown(f"""
            <div class="metric-card">
                <h3>💔 Tipo Dolor</h3>
                <div class="value-text">{dolor_texto}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            slope_texto = {
                "Flat": "Plana",
                "Up": "Ascendente",
                "Down": "Descendente"
            }[st_slope]
            st.markdown(f"""
            <div class="metric-card">
                <h3>📉 Pendiente ST</h3>
                <div class="value-text">{slope_texto}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Probabilidad Sin Enfermedad", f"{probs[0]*100:.1f}%")
        with col2:
            st.metric("Probabilidad Con Enfermedad", f"{probs[1]*100:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Recomendaciones Médicas")
        
        if clasificacion == "Alto Riesgo":
            st.markdown("""
            <div class="warning-box">
                <strong>⚠️ Acciones Recomendadas:</strong>
                <ul>
                    <li>Evaluación cardiológica completa de forma urgente</li>
                    <li>Electrocardiograma de 12 derivaciones</li>
                    <li>Ecocardiograma y prueba de esfuerzo supervisada</li>
                    <li>Analítica completa incluyendo perfil lipídico</li>
                    <li>Considerar derivación a unidad de cardiología</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <strong>✓ Recomendaciones Preventivas:</strong>
                <ul>
                    <li>Mantener seguimiento cardiológico anual</li>
                    <li>Dieta saludable baja en grasas saturadas</li>
                    <li>Ejercicio regular (150 min/semana mínimo)</li>
                    <li>Control periódico de presión arterial y colesterol</li>
                    <li>Evitar tabaco y reducir consumo de alcohol</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: white; 
            padding: 2rem; 
            border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 2rem 0;
            border-top: 5px solid #E63946;">
    
        <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #1A1A1A; font-size: 2rem; font-weight: 700; margin: 0; display: flex; align-items: center; justify-content: center; gap: 1rem;">
            Comience su Evaluación Cardiovascular 
            <span style="font-size: 2.5rem; animation: heartbeat 1s infinite; display: inline-block;">❤️</span>
        </h2>
        </div>
    
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-top: 1.5rem;">
        
        <div style="text-align: center; padding: 1.5rem; background: #F8F9FA; border-radius: 10px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📋</div>
            <h3 style="color: #E63946; font-size: 1.1rem; margin: 0.5rem 0;">Paso 1</h3>
            <p style="color: #666; font-size: 0.95rem; margin: 0;">Complete el formulario lateral</p>
        </div>
        
        <div style="text-align: center; padding: 1.5rem; background: #F8F9FA; border-radius: 10px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
            <h3 style="color: #E63946; font-size: 1.1rem; margin: 0.5rem 0;">Paso 2</h3>
            <p style="color: #666; font-size: 0.95rem; margin: 0;">Presione Analizar Riesgo</p>
        </div>
        
        <div style="text-align: center; padding: 1.5rem; background: #F8F9FA; border-radius: 10px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <h3 style="color: #E63946; font-size: 1.1rem; margin: 0.5rem 0;">Paso 3</h3>
            <p style="color: #666; font-size: 0.95rem; margin: 0;">Visualice los resultados</p>
        </div>
        
        </div>
        </div>
        """, unsafe_allow_html=True)
                
with tab2:
    if analizar:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Medidor de Riesgo")
            fig_gauge = crear_gauge_chart(probabilidad)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.subheader("🕸️ Análisis de Factores")
            fig_radar = crear_radar_chart(datos_paciente)
            st.plotly_chart(fig_radar, use_container_width=True)
        
        st.subheader("Resumen de Parámetros")
        
        tipo_dolor_texto = {'ASY': 'Asintomático', 'ATA': 'Angina Atípica', 'NAP': 'Dolor No Anginoso', 'TA': 'Angina Típica'}[chest_pain_type]
        pendiente_texto = {'Flat': 'Plana', 'Up': 'Ascendente', 'Down': 'Descendente'}[st_slope]
        # Crear tabla HTML personalizada en lugar de st.dataframe
        tabla_html = f"""
        <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden;">
           <thead>
              <tr style="background: #F5F5F5;">
                   <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #E0E0E0;">Parámetro</th>
                   <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #E0E0E0;">Valor</th>
                   <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #E0E0E0;">Estado</th>
              </tr>
            </thead>
            <tbody>
               <tr>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Edad</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{age} años</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Riesgo' if age > 60 else '✓ Normal'}</td>
               </tr>
               <tr>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Sexo</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{sex}</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">-</td>
              </tr>
              <tr>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Frecuencia Cardíaca Máxima</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{max_hr} bpm</td>
                <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Baja' if max_hr < (220 - age) * 0.6 else '✓ Adecuada'}</td>
              </tr>
              <tr>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Glucosa en Ayunas</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{"Sí (>120 mg/dl)" if fasting_bs == 1 else "No (<120 mg/dl)"}</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Elevada' if fasting_bs == 1 else '✓ Normal'}</td>
              </tr>
              <tr>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Angina por Ejercicio</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{exercise_angina}</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Presente' if exercise_angina == "Sí" else '✓ Ausente'}</td>
              </tr>
              <tr>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Tipo de Dolor Torácico</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{tipo_dolor_texto}</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Alto Riesgo' if chest_pain_type == "ASY" else '⚠️ Moderado' if chest_pain_type in ["TA", "ATA"] else '✓ Bajo'}</td>
              </tr>
              <tr>
                 <td style="padding: 1rem;">Pendiente del Segmento ST</td>
                 <td style="padding: 1rem;">{pendiente_texto}</td>
                 <td style="padding: 1rem;">{'⚠️ Anormal' if st_slope in ["Flat", "Down"] else '✓ Normal'}</td>
              </tr>
            </tbody>
        </table>
        """

        st.markdown(tabla_html, unsafe_allow_html=True)
    else:
        st.info("Complete los datos del paciente para ver las visualizaciones.")

with tab3:
    st.subheader("Historial de Pacientes")
    
    # Cargar historial
    df_historial = cargar_historial()
    
    if len(df_historial) == 0:
        st.info(" No hay registros todavía. Analiza un paciente para comenzar el historial.")
    else:
        # Estadísticas generales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📋 Total Pacientes", len(df_historial))
        
        with col2:
            alto_riesgo = len(df_historial[df_historial['Riesgo'] == 'ALTO'])
            st.metric("⚠️ Alto Riesgo", alto_riesgo)
        
        with col3:
            bajo_riesgo = len(df_historial[df_historial['Riesgo'] == 'BAJO'])
            st.metric("✅ Bajo Riesgo", bajo_riesgo)
        
        with col4:
            promedio_prob = df_historial['Probabilidad_%'].mean()
            st.metric("📊 Prob. Media", f"{promedio_prob:.1f}%")
        
        st.markdown("---")
        
        # Filtros
        st.subheader(" Filtros")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_riesgo = st.selectbox(
                "Filtrar por Riesgo",
                ["Todos", "ALTO", "BAJO"]
            )
        
        with col2:
            filtro_sexo = st.selectbox(
                "Filtrar por Sexo",
                ["Todos", "M", "F"]
            )
        
        with col3:
            ordenar_por = st.selectbox(
                "Ordenar por",
                ["Fecha (Reciente)", "Fecha (Antigua)", "Probabilidad (Mayor)", "Probabilidad (Menor)"]
            )
        
        # Aplicar filtros
        df_filtrado = df_historial.copy()
        
        if filtro_riesgo != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Riesgo'] == filtro_riesgo]
        
        if filtro_sexo != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Sexo'] == filtro_sexo]
        
        # Ordenar
        if ordenar_por == "Fecha (Reciente)":
            df_filtrado = df_filtrado.sort_values(['Fecha', 'Hora'], ascending=False)
        elif ordenar_por == "Fecha (Antigua)":
            df_filtrado = df_filtrado.sort_values(['Fecha', 'Hora'], ascending=True)
        elif ordenar_por == "Probabilidad (Mayor)":
            df_filtrado = df_filtrado.sort_values('Probabilidad_%', ascending=False)
        else:
            df_filtrado = df_filtrado.sort_values('Probabilidad_%', ascending=True)
        
        st.markdown("---")
        
        # Mostrar tabla
        st.subheader(f"📋 Registros ({len(df_filtrado)} pacientes)")
         
        # Crear tabla HTML para evitar error de PyArrow
        if len(df_filtrado) > 0:
            tabla_historial = "<div style='overflow-x: auto;'><table style='width: 100%; border-collapse: collapse; background: white; border-radius: 8px;'>"
    
            # Header
            tabla_historial += "<thead><tr style='background: #F5F5F5;'>"
            for col in df_filtrado.columns:
                tabla_historial += f"<th style='padding: 0.8rem; text-align: left; border-bottom: 2px solid #E0E0E0; font-size: 0.9rem;'>{col}</th>"
            tabla_historial += "</tr></thead><tbody>"
    
            # Rows
            for idx, row in df_filtrado.iterrows():
                # Color de fondo según riesgo
                bg_color = "#FFE5E5" if row['Riesgo'] == 'ALTO' else "#E8F5E9"
                tabla_historial += f"<tr style='background: {bg_color};'>"
        
                for col in df_filtrado.columns:
                    valor = str(row[col])
                    # Resaltar probabilidad si es alta
                    if col == 'Probabilidad_%':
                       prob = float(valor)
                       color = '#E63946' if prob >= 50 else '#06D6A0'
                       valor = f"<strong style='color: {color};'>{valor}%</strong>"
                    # Resaltar clasificación
                    elif col == 'Clasificacion':
                         color = '#E63946' if row['Riesgo'] == 'ALTO' else '#06D6A0'
                         valor = f"<strong style='color: {color};'>{valor}</strong>"
            
                    tabla_historial += f"<td style='padding: 0.8rem; border-bottom: 1px solid #F0F0F0; font-size: 0.85rem;'>{valor}</td>"
        
                tabla_historial += "</tr>"
    
            tabla_historial += "</tbody></table></div>"
    
            st.markdown(tabla_historial, unsafe_allow_html=True)
        else:
            st.info("No hay registros con los filtros aplicados")
        
        st.markdown("---")
        
        # Botón de descarga
        st.subheader("💾 Exportar Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Exportar CSV
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Historial Completo (CSV)",
                data=csv,
                file_name=f'historial_pacientes_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
            )
        
        with col2:
            # Exportar solo filtrados
            if len(df_filtrado) < len(df_historial):
                csv_filtrado = df_filtrado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar Filtrados (CSV)",
                    data=csv_filtrado,
                    file_name=f'historial_filtrado_{datetime.now().strftime("%Y%m%d")}.csv',
                    mime='text/csv',
                )
        
        # Gráfico de distribución
        st.markdown("---")
        st.subheader("📈 Distribución de Riesgo")
        
        import plotly.express as px
        
        fig = px.pie(
            df_historial, 
            names='Riesgo',
            title='Distribución de Pacientes por Nivel de Riesgo',
            color='Riesgo',
            color_discrete_map={'ALTO': '#E63946', 'BAJO': '#06D6A0'}
        )
        
        fig.update_layout(
            paper_bgcolor='white',
            font={'family': 'Inter'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.info("⚕️ **Nota Médica**: Este sistema es una herramienta de apoyo diagnóstico. Las decisiones clínicas finales deben ser tomadas por profesionales médicos cualificados.")

