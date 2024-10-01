import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page Streamlit
st.set_page_config(page_title="Abaque de Smith Interactif", page_icon=":satellite:", layout="wide")
st.title("Abaque de Smith Interactif pour l'Analyse RF")
st.markdown("**Un outil puissant pour visualiser et analyser les circuits RF**")

# Fonctions utilitaires
def calculer_gamma(Z, Z0):
    """Calcule le coefficient de réflexion Gamma."""
    return (Z - Z0) / (Z + Z0)

def calculer_impedance(Gamma, Z0):
    """Calcule l'impédance Z à partir de Gamma."""
    return Z0 * (1 + Gamma) / (1 - Gamma)

def calculer_delta_k(S11, S12, S21, S22):
    """Calcule Delta et K pour la stabilité."""
    Delta = (1 - S11 * S22 + S12 * S21) * (1 - S11 * S22 + S12 * S21) - (S11 * S21 * S12 * S22)
    K = (1 - abs(S11)**2 - abs(S22)**2 + abs(S11 * S22 - S12 * S21)**2) / (2 * abs(S21 * S12))
    return Delta, K

# Paramètres d'entrée
st.sidebar.header("Paramètres d'entrée")
Z0 = st.sidebar.number_input("Impédance caractéristique (Z0)", value=50.0)

choix_mode = st.sidebar.radio("Mode de saisie:", ("Impédance (Z)", "Coefficient de réflexion (Γ)"))

if choix_mode == "Impédance (Z)":
    Z_real = st.sidebar.number_input("Partie réelle de Z", value=100.0)
    Z_imag = st.sidebar.number_input("Partie imaginaire de Z", value=50.0)
    Gamma = calculer_gamma(complex(Z_real, Z_imag), Z0)
else:
    Gamma_mag = st.sidebar.number_input("Magnitude de Γ", value=0.5, min_value=0.0, max_value=1.0)
    Gamma_phase = st.sidebar.number_input("Phase de Γ (degrés)", value=45.0)
    Gamma = Gamma_mag * np.exp(1j * np.deg2rad(Gamma_phase))
    Z = calculer_impedance(Gamma.conj(), Z0.real)

# Affichage des résultats
st.subheader("Résultats")
st.write(f"**Impédance (Z):** {Z:.2f} Ω")
st.write(f"**Coefficient de réflexion (Γ):** {Gamma:.2f}")

# Tracé de l'abaque de Smith
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

# Cercles de résistance constante
for R in np.arange(0, 5.1, 0.5):
    center = (R/(R+1), 0) # Correct center calculation for constant resistance circles
    radius = 1/(R+1)  # Correct radius calculation 
    theta = np.linspace(0, 2*np.pi, 200)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax.plot(theta, np.sqrt(x**2 + y**2), 'k-', linewidth=0.5)
    if R <= 2.0 :
        ax.text(np.pi/2, R/(R+1), f'R={R:.1f}', ha='center', va='center', fontsize=8)

# Cercles de réactance constante (arcs)
for X in np.arange(-5, 5.1, 0.5):
    center = (1, 1/X) if X != 0 else (1, float('inf')) # Correct center for constant reactance arcs
    radius = 1/abs(X) if X != 0 else float('inf') # Correct radius
    start_angle = np.arctan(-1/X) if X != 0 else np.pi/2
    end_angle = np.arctan(1/X) if X != 0 else 3*np.pi/2
    theta = np.linspace(start_angle, end_angle, 200)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    ax.plot(theta, np.sqrt(x**2 + y**2), 'k-', linewidth=0.5)
    if abs(X) <= 2.0 and X != 0:
        ax.text(np.pi, 1 / abs(X), f'X={X:.1f}', ha='center', va='center', fontsize=8)

# Point d'impédance
ax.plot(np.angle(Gamma), abs(Gamma), 'ro', markersize=8, label='Point Z/Γ')

# Configuration de l'abaque
ax.set_theta_zero_location("N")  # Angle zéro en haut
ax.set_theta_direction(-1)  # Sens inverse des aiguilles d'une montre
ax.set_rlim(0, 1.2)  # Limite du rayon
ax.set_title("Abaque de Smith", fontsize=14)
ax.grid(True)
ax.legend()

# Affichage de l'abaque
st.pyplot(fig)

# Analyse de la stabilité (facultatif)
st.sidebar.header("Analyse de la stabilité (Optionnel)")
analyse_stabilite = st.sidebar.checkbox("Activer l'analyse de stabilité")

if analyse_stabilite:
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
    elif abs(Delta) > 1 and K < 1:
        st.write("**Le circuit est stable conditionnellement.**")
    else:
        st.write("**Le circuit est instable.**")