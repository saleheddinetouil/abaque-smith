import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from shapely.geometry import Point, LineString, Polygon

st.set_page_config(page_title="Abaque de Smith Interactif", page_icon=":satellite:", layout="wide")
st.title("Abaque de Smith Interactif pour l'Analyse RF")
st.markdown("**Un outil puissant pour visualiser et analyser les circuits RF**")

# Paramètres
Z0 = 50  # Impédance caractéristique

# Fonctions utilitaires
def calculer_gamma(Z, Z0):
    return (Z - Z0) / (Z + Z0)

def calculer_impedance(gamma, Z0):
    return Z0 * (1 + gamma) / (1 - gamma)

def tracer_abaque(ax):
    # Cercles de résistance constante
    for R in np.arange(0.1, 5.1, 0.5):
        theta = np.linspace(0, 2 * np.pi, 200)
        x = (1 - R) / (1 + R) * np.cos(theta) + 1
        y = (1 - R) / (1 + R) * np.sin(theta)
        ax.plot(x, y, 'k-', linewidth=0.5)
        if R <= 2.0:
            ax.text(x[len(x)//2], y[len(y)//2], f"R={R:.1f}", ha='center', va='center')

    # Cercles de réactance constante
    for X in np.arange(-5, 5.1, 0.5):
        theta = np.linspace(np.pi/2 + 0.1, 3*np.pi/2 -0.1, 100) if X > 0 else np.linspace(3*np.pi/2 + 0.1, 5*np.pi/2 - 0.1, 100) # correction de trace
        if X >0 :
            x = (1/(X + 1))* np.cos(theta) + 1
            y = (1/(X + 1))*np.sin(theta)

        else :
            x = (1/( - X + 1))* np.cos(theta) + 1
            y = (1/( - X + 1))* np.sin(theta)


        ax.plot(x,y,'k-',linewidth = 0.5)

    #Axes et titre
    ax.set_xlabel('Partie Réelle')
    ax.set_ylabel('Partie Imaginaire')
    ax.set_aspect('equal')
    ax.set_title('Abaque de Smith')

def impédance_utilisateur():
    z_real = st.number_input("Partie réelle de Z", value=50.0,step=1)
    z_imag = st.number_input("Partie imaginaire de Z", value=0.0, step=1)
    z_user = z_real + z_imag*1j

    return z_user

def reflection_utilisateur():
    mag = st.number_input('Magnitude du Coefficient de Réflexion',value=0.5, min_value=0,max_value=1)
    phase = st.number_input('Phase (degrés)',value=0.0)
    ref_user = mag * np.exp(1j * np.deg2rad(phase))

    return ref_user


# Layout
col1, col2 = st.columns(2)
choix = col1.radio("Mode de saisie :", ["Impédance", "Coefficient de Réflexion"])

if choix == 'Impédance':
    z_user = impédance_utilisateur()
    gamma_user = calculer_gamma(z_user, Z0)

    col1.markdown("**Valeur de l'impédance:** ")
    col1.markdown(f"{z_user:.2f} Ω")
    col2.markdown("**Coefficient de Réflexion :**")
    col2.markdown(f"{gamma_user:.2f}")

elif choix == 'Coefficient de Réflexion':
    gamma_user = reflection_utilisateur()
    z_user = calculer_impedance(gamma_user,Z0)

    col2.markdown("**Impédance:** ")
    col2.markdown(f"{z_user:.2f} Ω")
    col1.markdown("**Valeur du coefficient de réflexion:**")
    col1.markdown(f"{gamma_user:.2f}")

# graphique
fig, ax = plt.subplots(figsize=(6, 6))

tracer_abaque(ax)
ax.plot(gamma_user.real, gamma_user.imag, 'rx', markersize=10,label = 'Votre Point')
ax.legend()

st.pyplot(fig)



st.write("**Important :** Les intersections et autres points doivent être trouvés algorithmiquement  avec des librairies mathématiques.")

st.write("**Remarque :** Le projet demande une robustesse avancée du programme.")