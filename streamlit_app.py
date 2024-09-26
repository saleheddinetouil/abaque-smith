import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def tracer_abaque_smith(S11, S12, S21, S22, Gamma_L, Gamma_G):
    """
    Trace l'abaque de Smith avec les cercles de résistance, de réactance,
    les impédances d'entrée et de sortie, les points Gamma, et les cercles Γin et Γout.
    """

    # Calcul des coefficients de réflexion à l'entrée et à la sortie
    Gamma_in = S11 + (S12 * S21 * Gamma_L) / (1 - S22 * Gamma_L)
    Gamma_out = S22 + (S12 * S21 * Gamma_G) / (1 - S11 * Gamma_G)

    # Calcul des impédances normalisées
    Z_in = (1 + Gamma_in) / (1 - Gamma_in)
    Z_out = (1 + Gamma_out) / (1 - Gamma_out)

    # Conversion en coordonnées polaires
    r_in = np.abs(Z_in)
    theta_in = np.angle(Z_in)
    r_out = np.abs(Z_out)
    theta_out = np.angle(Z_out)

    # Calcul du delta et du K
    Delta = (1 - S11 * S22 + S12 * S21) * (1 - S11 * S22 + S12 * S21) - (S11 * S21 * S12 * S22)
    K = (1 - abs(S11)**2 - abs(S22)**2 + abs(S11 * S22 - S12 * S21)**2) / (2 * abs(S21 * S12))

    # Vérification de la stabilité du circuit
    st.write(f"**Delta:** {Delta}")
    st.write(f"**K:** {K}")
    if abs(Delta) > 1 and abs(K) < 1:
        st.write("**Le circuit est stable inconditionnellement.**")
    elif abs(Delta) > 1 and abs(K) > 1:
        st.write("**Le circuit est stable conditionnellement.**")
    else:
        st.write("**Le circuit est instable.**")

    # Création de l'abaque de Smith
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # Trace des cercles de résistance constante
    for R in np.arange(0.1, 2.1, 0.1):
        theta = np.linspace(0, 2 * np.pi, 100)
        r = R / (R + 1)  # Correction de la formule pour le rayon
        x = r * np.cos(theta) + (1 - r)  # Décalage du centre du cercle
        y = r * np.sin(theta)
        ax.plot(theta, np.sqrt(x**2 + y**2), 'k-', linewidth=0.5)  # Tracé en coordonnées polaires
        ax.text(np.pi / 2, R, f'R={R:.1f}', ha='center', va='center', fontsize=8)

    # Trace des cercles de réactance constante
    for X in np.arange(-2, 2.1, 0.2):
        theta = np.linspace(0, 2 * np.pi, 100)
        r = 1 / np.abs(X)  # Correction de la formule pour le rayon
        x = r * np.cos(theta)
        y = r * np.sin(theta) + 1 / X if X != 0 else float('inf')  # Décalage du centre du cercle
        ax.plot(theta, np.sqrt(x**2 + y**2), 'k-', linewidth=0.5)  # Tracé en coordonnées polaires
        ax.text(np.pi, 1 / np.abs(X), f'X={X:.1f}', ha='center', va='center', fontsize=8)


    # Trace des points pour les impédances d'entrée et de sortie
    ax.plot(theta_in, r_in, 'ro-', label='Impédance d\'entrée')
    ax.plot(theta_out, r_out, 'bo-', label='Impédance de sortie')

    # Trace des points Gamma_in et Gamma_out
    ax.plot(np.angle(Gamma_in), np.abs(Gamma_in), 'rx', markersize=10, label='Gamma_in')
    ax.plot(np.angle(Gamma_out), np.abs(Gamma_out), 'bx', markersize=10, label='Gamma_out')

    # Trace du cercle Γin en coordonnées polaires
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(theta, np.abs(Gamma_in) * np.ones_like(theta), 'r--', label='Cercle Γin')

    # Trace du cercle Γout en coordonnées polaires
    ax.plot(theta, np.abs(Gamma_out) * np.ones_like(theta), 'b--', label='Cercle Γout')

    # Configuration de l'abaque
    ax.set_theta_zero_location("N")  # Angle zéro en haut
    ax.set_theta_direction(-1)  # Sens inverse des aiguilles d'une montre
    ax.set_rlim(0, 2)  # Limite du rayon
    ax.set_title("Abaque de Smith")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


# Données démo pour les 3 cas de stabilité
donnees_demo = {
    "stable_inconditionnellement": {
        "S11": 0.5 + 0.3j, "S12": 0.1 + 0.05j, "S21": 2 + 1j, "S22": 0.2 + 0.1j,
        "Gamma_L": 0.2 + 0.1j, "Gamma_G": 0.3 + 0.2j
    },
    "stable_conditionnellement": {
        "S11": 0.8 + 0.5j, "S12": 0.2 + 0.1j, "S21": 1.5 + 0.8j, "S22": 0.6 + 0.4j,
        "Gamma_L": 0.2 + 0.1j, "Gamma_G": 0.3 + 0.2j
    },
    "instable": {
        "S11": 1.2 + 0.8j, "S12": 0.3 + 0.2j, "S21": 0.5 + 0.3j, "S22": 1.1 + 0.7j,
        "Gamma_L": 0.2 + 0.1j, "Gamma_G": 0.3 + 0.2j
    }
}

# Titre de l'application
st.title("Abaque de Smith Interactif")

# Choix du mode d'entrée des données
mode = st.radio("Choisissez le mode d'entrée des données:",
                 ("Données démo", "Saisie manuelle"))

if mode == "Données démo":
    cas = st.selectbox("Choisissez le cas de stabilité à afficher:",
                       ("Stable inconditionnellement", "Stable conditionnellement", "Instable"))

    donnees = donnees_demo[cas.replace(" ", "_")]
    tracer_abaque_smith(**donnees)

elif mode == "Saisie manuelle":
    # Saisie manuelle des coefficients de la matrice S et des coefficients de réflexion
    st.subheader("Coefficients de la matrice S")
    S11 = complex(st.text_input("Entrez S11 (ex: 0.5+0.3j): ", "0.5+0.3j"))
    S12 = complex(st.text_input("Entrez S12 (ex: 0.2+0.1j): ", "0.2+0.1j"))
    S21 = complex(st.text_input("Entrez S21 (ex: 0.8+0.4j): ", "0.8+0.4j"))
    S22 = complex(st.text_input("Entrez S22 (ex: 0.3+0.2j): ", "0.3+0.2j"))

    st.subheader("Coefficients de réflexion")
    Gamma_L = complex(st.text_input("Entrez Gamma_L (ex: 0.2+0.1j): ", "0.2+0.1j"))
    Gamma_G = complex(st.text_input("Entrez Gamma_G (ex: 0.3+0.2j): ", "0.3+0.2j"))

    tracer_abaque_smith(S11, S12, S21, S22, Gamma_L, Gamma_G)