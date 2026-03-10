# ❤️ CardioPredict Pro — Predicción de Enfermedades Cardíacas

> Sistema de Machine Learning para la predicción del riesgo cardiovascular basado en datos clínicos de pacientes.

🌐 **Aplicación en producción:** [https://project-6-team-4-ml.onrender.com/](https://project-6-team-4-ml.onrender.com/)

<p align="center">
  <a href="https://project-6-team-4-ml.onrender.com/">
    <img src="src/img/qr_app.png" alt="QR CardioPredict Pro" width="180"/>
  </a>
</p>

---

## 📋 Descripción General

**CardioPredict Pro** es un proyecto de Machine Learning completo de extremo a extremo que predice el riesgo de enfermedad cardíaca utilizando un conjunto de datos clínicos de 918 pacientes. El proyecto cubre todo el flujo de trabajo de ML: análisis exploratorio de datos (EDA), preprocesamiento, entrenamiento de modelos, evaluación y despliegue como aplicación web interactiva.

---

## 🚀 Funcionalidades

- 🔬 **EDA completo** con análisis estadístico y análisis de supervivencia (Kaplan-Meier y modelo de Cox)
- 🤖 **Modelos ML entrenados**: Regresión Logística, Random Forest, K-NN y XGBoost
- 📊 **Dashboard interactivo** desarrollado con Streamlit
- 🗂️ **Historial de pacientes** con exportación en CSV
- 🐳 **Soporte Docker** para despliegue sencillo
- ⚙️ **Pipeline CI/CD** mediante GitHub Actions

---

## 📁 Estructura del Proyecto

```
project-6-team-4-ml/
├── app.py                          # Aplicación web con Streamlit
├── data/
│   ├── heart.csv                   # Dataset original (918 pacientes × 12 variables)
│   ├── heart_procesado_g.csv       # Dataset procesado por Gema
│   ├── heart_procesado_i.csv       # Dataset procesado por Isrodam
│   └── heart_processed_R.csv       # Dataset procesado por Roberto
├── models/
│   ├── modelo_coronario.pkl        # Modelo final entrenado
│   └── scaler_coronario.pkl        # Escalador de variables
├── notebook/
│   ├── eda_heart_disease_p.ipynb   # EDA + Análisis de Supervivencia (Paloma)
│   ├── eda_heart_failure_g.ipynb   # EDA (Gema)
│   ├── eda_heart_failure_i.ipynb   # EDA (Isrodam)
│   ├── eda_heart_failure_R.ipynb   # EDA (Roberto)
│   ├── entrenamiento_modelo_final.ipynb
│   ├── entrenamiento_modelo_g.ipynb
│   └── entrenamiento_modelo_i.ipynb
├── report/
│   ├── entrenamiento_modelo_final.pdf
│   ├── Informe_evaluacion_g.pdf
│   ├── Informe_evaluacion_i.pdf
│   └── report_R_pdf.pdf
├── docs/
│   └── historial_pacientes.csv
├── src/
│   └── img/
│       └── qr_app.png              # QR code de la aplicación
├── assets/
├── dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

---

## 📊 Dataset

El dataset contiene **918 registros de pacientes** con las siguientes variables:

| Variable | Descripción | Tipo |
|----------|-------------|------|
| `Age` | Edad del paciente | Numérica |
| `Sex` | Sexo (M/F) | Categórica |
| `ChestPainType` | Tipo de dolor torácico (ATA, NAP, ASY, TA) | Categórica |
| `RestingBP` | Presión arterial en reposo (mm Hg) | Numérica |
| `Cholesterol` | Colesterol sérico (mg/dl) | Numérica |
| `FastingBS` | Azúcar en sangre en ayunas > 120 mg/dl (0/1) | Binaria |
| `RestingECG` | Resultados del ECG en reposo | Categórica |
| `MaxHR` | Frecuencia cardíaca máxima alcanzada | Numérica |
| `ExerciseAngina` | Angina inducida por ejercicio (Y/N) | Binaria |
| `Oldpeak` | Depresión del segmento ST | Numérica |
| `ST_Slope` | Pendiente del segmento ST | Categórica |
| `HeartDisease` | **Variable objetivo** — Enfermedad cardíaca (0/1) | Binaria |

---

## ⚙️ Instalación y Configuración

### Requisitos previos
- Python `>=3.11, <3.13`
- Gestor de paquetes [`uv`](https://docs.astral.sh/uv/)

### 🔹 macOS / Linux

```bash
# Instalar uv (si no está instalado)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear y activar el entorno virtual
uv venv
source .venv/bin/activate

# Instalar dependencias
uv sync
```

### 🔹 Windows (PowerShell o CMD)

```bash
# Instalar uv (si no está instalado)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Crear y activar el entorno virtual
uv venv
.venv\Scripts\activate

# Instalar dependencias
uv sync
```

---

## ▶️ Ejecutar la Aplicación

```bash
streamlit run app.py
```

A continuación, abre tu navegador en [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build
```

---

## 🧪 Tests

```bash
pytest
```

---

## 🤖 Modelos Evaluados y Selección del Modelo Final

Durante el proyecto se entrenaron y compararon cuatro algoritmos de clasificación sobre el mismo conjunto de datos preprocesado:

| Modelo | Accuracy | Recall (clase 1) | ROC-AUC | Observaciones |
|--------|----------|------------------|---------|---------------|
| **Regresión Logística** *(umbral 0.4)* | **88 %** | **0.94** | **0.926** | ✅ Modelo seleccionado |
| Random Forest | ~87 % | ~0.88 | ~0.91 | Mayor accuracy bruta, menor recall |
| K-Nearest Neighbors (K-NN) | ~82 % | ~0.83 | ~0.87 | Sensible a la escala, peor generalización |
| XGBoost | ~86 % | ~0.87 | ~0.90 | Buen rendimiento, menor interpretabilidad |

### ✅ ¿Por qué elegimos la Regresión Logística?

Aunque el **Random Forest** obtuvo una precisión global ligeramente superior, la **Regresión Logística con umbral ajustado a 0.4** fue elegida como modelo definitivo por tres razones clave para el entorno médico:

1. **Máximo Recall (0.94):** Reducir el umbral de 0.5 a 0.4 permite detectar al **94 % de los pacientes con riesgo coronario real**. En cardiología, un *falso negativo* (no detectar a un enfermo) tiene consecuencias mucho más graves que un *falso positivo* (realizar pruebas adicionales a un paciente sano).

2. **Robustez y ausencia de sobreajuste:** La diferencia entre la precisión en entrenamiento (86.1 %) y en test (88.0 %) es de apenas **0.007**, confirmando que el modelo generaliza correctamente y no memoriza los datos. La validación cruzada de 5 pliegues arrojó una precisión media del **84.74 %** con una desviación estándar del 2.91 %, ratificando su estabilidad.

3. **Transparencia clínica:** Al ser un modelo lineal, sus coeficientes permiten a los especialistas entender exactamente qué variables (tipo de dolor torácico, pendiente del ECG, azúcar en ayunas) están influyendo en cada predicción, facilitando la confianza en el diagnóstico asistido por IA.

> 📄 El análisis completo se encuentra en [`notebook/entrenamiento_modelo_final.ipynb`](notebook/entrenamiento_modelo_final.ipynb) y en el informe [`report/entrenamiento_modelo_final.pdf`](report/entrenamiento_modelo_final.pdf).

---

## 👥 Autores

| Nombre | GitHub |
|--------|--------|
| **Gema Y.C.** | [@gemayc](https://github.com/gemayc) |
| **Roberto Molero Losada** | [@iRuperth](https://github.com/iRuperth) |
| **Isrodam** | [@isrodam](https://github.com/isrodam) |
| **Paloma** | [@Pal-cloud](https://github.com/Pal-cloud) |

---

## 📄 Licencia

Este proyecto fue desarrollado como parte del programa **Bootcamp IA P6**.
