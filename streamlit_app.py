import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pySmithPlot.SmithPlot import SmithPlot

st.title("Abaque de Smith Interactif avec pySmithPlot")

# Paramètres de l'abaque de Smith
show_circles = st.checkbox("Afficher les cercles de résistance/réactance", value=True)
show_labels = st.checkbox("Afficher les labels des cercles", value=True)

# Coefficients de la matrice S
st.subheader("Coefficients de la matrice S")
S11 = complex(st.text_input("Entrez S11 (ex: 0.5+0.3j): ", "0.5+0.3j"))
S12 = complex(st.text_input("Entrez S12 (ex: 0.2+0.1j): ", "0.2+0.1j"))
S21 = complex(st.text_input("Entrez S21 (ex: 0.8+0.4j): ", "0.8+0.4j"))
S22 = complex(st.text_input("Entrez S22 (ex: 0.3+0.2j): ", "0.3+0.2j"))

# Coefficients de réflexion
st.subheader("Coefficients de réflexion")
Gamma_L = complex(st.text_input("Entrez Gamma_L (ex: 0.2+0.1j): ", "0.2+0.1j"))
Gamma_G = complex(st.text_input("Entrez Gamma_G (ex: 0.3+0.2j): ", "0.3+0.2j"))

# Calcul des coefficients de réflexion à l'entrée et à la sortie
Gamma_in = S11 + (S12 * S21 * Gamma_L) / (1 - S22 * Gamma_L)
Gamma_out = S22 + (S12 * S21 * Gamma_G) / (1 - S11 * Gamma_G)

# Calcul des impédances normalisées
Z_in = (1 + Gamma_in) / (1 - Gamma_in)
Z_out = (1 + Gamma_out) / (1 - Gamma_out)

# Création de l'abaque de Smith
sp = SmithPlot(show_circles=show_circles, show_labels=show_labels)

# Trace des points pour les impédances d'entrée et de sortie
sp.plot_point(Z_in.real, Z_in.imag, label='Impédance d\'entrée', marker='o', color='r')
sp.plot_point(Z_out.real, Z_out.imag, label='Impédance de sortie', marker='o', color='b')

# Trace des points Gamma_in et Gamma_out
sp.plot_point(Gamma_in.real, Gamma_in.imag, label='Gamma_in', marker='x', color='r')
sp.plot_point(Gamma_out.real, Gamma_out.imag, label='Gamma_out', marker='x', color='b')

# Trace du cercle Γin 
sp.plot_circle(center=S11, radius=abs((S12*S21)/(1-S22*Gamma_L)), label='Cercle Γin', color='r', linestyle='--')

# Trace du cercle Γout 
sp.plot_circle(center=S22, radius=abs((S12*S21)/(1-S11*Gamma_G)), label='Cercle Γout', color='b', linestyle='--')


# Affichage de l'abaque de Smith
st.pyplot(sp.get_figure())

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