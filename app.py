import streamlit as st
import pandas as pd
import numpy as np
import data_loader as dl
import engine_var as ev
import backtesting as bt
import reporting as rp
import os

# Configuration de la page
st.set_page_config(page_title="VaR Progiciel - Ecclesiaste", layout="wide")

st.title("📊 Terminal de Gestion des Risques (VaR)")
st.markdown("""
Développé par **Écclésiaste GNARGO** - Spécialité IFIM.  
Ce progiciel permet de calculer et comparer 7 méthodes de Value-at-Risk.
""")

# --- BARRE LATÉRALE (Paramètres) ---
st.sidebar.header("Configuration du Portefeuille")
tickers_input = st.sidebar.text_input("Tickers (séparés par virgule)", "MC.PA, TTE.PA, BNP.PA")
start_date = st.sidebar.date_input("Date de début", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("Date de fin", pd.to_datetime("2026-04-01"))
conf_level = st.sidebar.slider("Niveau de Confiance", 0.90, 0.99, 0.95)

if st.sidebar.button("Lancer l'Analyse"):
    tickers = [t.strip().upper() for t in tickers_input.split(',')]
    
    with st.spinner('Récupération des données et calculs en cours...'):
        # 1. Chargement
        prices, returns = dl.get_portfolio_data(tickers, start_date, end_date)
        
        # Affichage du graphique de performance
        st.subheader("📈 Performance du Portefeuille")
        st.line_chart(prices)

        # 2. Calculs & Backtesting
        test_returns = returns.iloc[-250:]
        methods = ['Historique', 'Paramétrique', 'Cornish-Fisher', 'Risk-Metrics', 'GARCH', 'TVE', 'TVE-Garch']
        summary = []

        for m in methods:
            forecasts = []
            # On simule sur les 20 derniers jours pour la rapidité de la démo Web
            for i in range(len(test_returns[-20:])): 
                hist = returns.iloc[:-(20-i)].iloc[-252:]
                engine = ev.VaREngine(hist, confidence_level=conf_level)
                
                if m == 'Historique': forecasts.append(engine.var_historical())
                elif m == 'Paramétrique': forecasts.append(engine.var_parametric())
                elif m == 'Cornish-Fisher': forecasts.append(engine.var_cornish_fisher())
                elif m == 'Risk-Metrics': forecasts.append(engine.var_riskmetrics())
                elif m == 'GARCH': forecasts.append(engine.var_garch())
                elif m == 'TVE': forecasts.append(engine.var_tve())
                else: forecasts.append(engine.var_tve_garch())
            
            tester = bt.VaRBacktester(test_returns[-20:], np.array(forecasts))
            p_kup, p_obs = tester.kupiec_test()
            summary.append({
                "Methode": m, 
                "Exceptions": tester.x, 
                "Taux Obs (%)": round(p_obs * 100, 2),
                "P_value": round(p_kup, 4),
                "Statut": "✅ Valide" if p_kup > 0.05 else "❌ Rejete"
            })

        # 3. Affichage des résultats
        st.subheader("🛡️ Résultats du Backtesting")
        df_res = pd.DataFrame(summary)
        
        # Style du tableau
        def color_statut(val):
            color = 'green' if 'Valide' in val else 'red'
            return f'color: {color}'
        
        st.table(df_res.style.applymap(color_statut, subset=['Statut']))

        # 4. Exportations
        st.subheader("📥 Télécharger les Rapports")
        col1, col2 = st.columns(2)
        
        # On génère les fichiers pour le téléchargement
        if not os.path.exists('outputs'): os.makedirs('outputs')
        rp.export_to_excel(df_res)
        rp.generate_pdf(df_res)

        with open("outputs/Reporting_VaR.xlsx", "rb") as f:
            col1.download_button("Excel Report", f, file_name="VaR_Report.xlsx")
            
        with open("outputs/Rapport_Direction.pdf", "rb") as f:
            col2.download_button("PDF Synthesis", f, file_name="Management_Summary.pdf")

    st.success("Analyse terminée avec succès !")