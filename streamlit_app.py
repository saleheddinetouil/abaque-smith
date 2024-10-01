import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Abaque de Smith Interactif", page_icon=":satellite:", layout="wide")
st.title("Abaque de Smith Interactif pour l'Analyse RF")
st.markdown("**Un outil puissant pour visualiser et analyser les circuits RF**")

def calculer_gamma(Z, Z0):
    return (Z - Z0) / (Z + Z0)

def calculer_impedance(Gamma, Z0):
    return Z0 * (1 + Gamma) / (1 - Gamma)

def calculer_delta_k(S11, S12, S21, S22):
    Delta = (1 - S11 * S22 + S12 * S21) * (1 - S11 * S22 + S12 * S21) - (S11 * S21 * S12 * S22)
    K = (1 - abs(S11)**2 - abs(S22)**2 + abs(S11 * S22 - S12 * S21)**2) / (2 * abs(S21 * S12))
    return Delta, K

st.sidebar.header("Paramètres d'entrée")
Z0 = st.sidebar.number_input("Impédance caractéristique (Z0)", value=50.0)
choix_mode = st.sidebar.radio("Mode de saisie:", ("Impédance (Z)", "Coefficient de réflexion (Γ)"))

st.subheader("Résultats")
if choix_mode == "Impédance (Z)":
    Z_real = st.sidebar.number_input("Partie réelle de Z", value=100.0)
    Z_imag = st.sidebar.number_input("Partie imaginaire de Z", value=50.0)
    Z = complex(Z_real, Z_imag)
    Gamma = calculer_gamma(Z, Z0)
    st.write(f"**Coefficient de réflexion (Γ):** {Gamma:.2f}")
else:
    Gamma_mag = st.sidebar.number_input("Magnitude de Γ", value=0.5, min_value=0.0, max_value=1.0)
    Gamma_phase = st.sidebar.number_input("Phase de Γ (degrés)", value=45.0)
    Gamma = Gamma_mag * np.exp(1j * np.deg2rad(Gamma_phase))
    Z = calculer_impedance(Gamma, Z0)
    st.write(f"**Impédance (Z):** {Z:.2f} Ω")

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

# Cercles de résistance constante
for R in np.arange(0.1, 2.1, 0.1):
    theta = np.linspace(0, 2 * np.pi, 200)
    radius = (1 - R) / (1 + R)
    ax.plot(theta, radius * np.ones_like(theta), 'k-', linewidth=0.5)  
    ax.text(np.pi / 2, radius, f'R={R:.1f}', ha='center', va='center', fontsize=8)

# Cercles de réactance constante
for X in np.arange(-2, 2.1, 0.2):
    theta = np.linspace(0, 2 * np.pi, 200)
    radius = 1/(1 + X**2)**0.5
    ax.plot(theta, radius * np.ones_like(theta), 'k-', linewidth=0.5)
    ax.text(np.pi, radius, f'X={X:.1f}', ha='center', va='center', fontsize=8)

# Point d'impédance (Z) ou coefficient de réflexion (Gamma)
r = abs(Gamma)
theta = np.angle(Gamma)
ax.plot(theta, r, 'ro', markersize=8, label=f'{"Point Z" if choix_mode=="Impédance (Z)" else "Point Γ"}')

# Configuration de l'abaque
ax.set_theta_zero_location("N")  
ax.set_theta_direction(-1)  
ax.set_rlim(0, 1)  
ax.set_title("Abaque de Smith", fontsize=14)
ax.grid(True)
ax.legend()
st.pyplot(fig)


if st.sidebar.checkbox("Afficher l'analyse de stabilité"):
    st.subheader("Analyse de la stabilité")
    S11 = complex(st.sidebar.text_input("Entrez S11 (ex: 0.5+0.3j): ", "0.5+0.3j"))
    S12 = complex(st.sidebar.text_input("Entrez S12 (ex: 0.2+0.1j): ", "0.2+0.1j"))
    S21 = complex(st.sidebar.text_input("Entrez S21 (ex: 0.8+0.4j): ", "0.8+0.4j"))
    S22 = complex(st.sidebar.text_input("Entrez S22 (ex: 0.3+0.2j): ", "0.3+0.2j"))

    Delta, K = calculer_delta_k(S11, S12, S21, S22)
    st.write(f"**Delta:** {Delta:.2f}")
    st.write(f"**K:** {K:.2f}")

    if abs(Delta) > 1 and K > 1:
        st.write("**Le circuit est stable inconditionnellement.**")
    elif abs(Delta) > 1:
        st.write("**Le circuit est stable conditionnellement.**")
    else:
        st.write("**Le circuit est instable.**")