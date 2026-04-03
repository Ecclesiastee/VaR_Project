"""import data_loader as dl
import engine_var as ev
import backtesting as bt
import reporting as rp
import pandas as pd
import numpy as np
import os

if not os.path.exists('outputs'): os.makedirs('outputs')

def main():
    tickers = ['MC.PA', 'TTE.PA', 'BNP.PA']
    prices, returns = dl.get_portfolio_data(tickers, '2023-01-01', '2026-01-01')
    
    test_returns = returns.iloc[-250:]
    methods = ['Historique', 'Paramétrique', 'Cornish-Fisher', 'Risk-Metrics', 'GARCH', 'TVE', 'TVE-Garch']
    summary = []

    for m in methods:
        forecasts = []
        for i in range(len(test_returns)):
            hist = returns.iloc[:-(len(test_returns)-i)].iloc[-252:]
            engine = ev.VaREngine(hist)
            if m == 'Historique': forecasts.append(engine.var_historical())
            elif m == 'Paramétrique': forecasts.append(engine.var_parametric())
            elif m == 'Cornish-Fisher': forecasts.append(engine.var_cornish_fisher())
            elif m == 'Risk-Metrics': forecasts.append(engine.var_riskmetrics())
            elif m == 'GARCH': forecasts.append(engine.var_garch())
            elif m == 'TVE': forecasts.append(engine.var_tve())
            else: forecasts.append(engine.var_tve_garch())
        
        tester = bt.VaRBacktester(test_returns, np.array(forecasts))
        p_kup, p_obs = tester.kupiec_test()
        p_ind = tester.christoffersen_test()
        summary.append({"Méthode": m, "Exceptions": tester.x, "Statut": "Validé" if p_kup > 0.05 else "Rejeté"})

    df_res = pd.DataFrame(summary)
    rp.export_to_excel(df_res)
    rp.generate_pdf(df_res)
    print("Travail terminé. Fichiers disponibles dans /outputs")

if __name__ == "__main__":
    main()"""
import data_loader as dl
import engine_var as ev
import backtesting as bt
import reporting as rp
import pandas as pd
import numpy as np
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    if not os.path.exists('outputs'): 
        os.makedirs('outputs')

    clear_screen()
    print("====================================================")
    print("   PROGICIEL DE GESTION DES RISQUES - VaR ENGINE    ")
    print("          Développé par Écclésiaste GNARGO          ")
    print("====================================================\n")

    # --- ÉTAPE 1 : INPUTS UTILISATEUR ---
    print("[1] Configuration du Portefeuille")
    user_input = input("Entrez les tickers séparés par une virgule (ex: MC.PA,TTE.PA,BNP.PA) : ")
    tickers = [t.strip().upper() for t in user_input.split(',')]
    
    start_date = input("Date de début (AAAA-MM-JJ, défaut 2023-01-01) : ") or "2023-01-01"
    end_date = input("Date de fin (AAAA-MM-JJ, défaut aujourd'hui) : ") or "2026-04-01"

    # --- ÉTAPE 2 : CHARGEMENT ---
    try:
        print(f"\n[2] Récupération des données pour {tickers}...")
        prices, returns = dl.get_portfolio_data(tickers, start_date, end_date)
    except Exception as e:
        print(f" Erreur lors du téléchargement : {e}")
        return

    # --- ÉTAPE 3 : CALCULS ---
    print("\n[3] Calcul des 7 modèles de VaR & Backtesting...")
    print("    (Cela peut prendre quelques secondes pour les modèles GARCH et TVE)")
    
    test_returns = returns.iloc[-250:] # Fenêtre de test d'un an environ
    methods = ['Historique', 'Paramétrique', 'Cornish-Fisher', 'Risk-Metrics', 'GARCH', 'TVE', 'TVE-Garch']
    summary = []

    for m in methods:
        sys.stdout.write(f"    -> Traitement de la méthode : {m} \r")
        sys.stdout.flush()
        
        forecasts = []
        for i in range(len(test_returns)):
            # Fenêtre glissante de 252 jours pour l'estimation
            hist = returns.iloc[:-(len(test_returns)-i)].iloc[-252:]
            engine = ev.VaREngine(hist)
            
            if m == 'Historique': forecasts.append(engine.var_historical())
            elif m == 'Paramétrique': forecasts.append(engine.var_parametric())
            elif m == 'Cornish-Fisher': forecasts.append(engine.var_cornish_fisher())
            elif m == 'Risk-Metrics': forecasts.append(engine.var_riskmetrics())
            elif m == 'GARCH': forecasts.append(engine.var_garch())
            elif m == 'TVE': forecasts.append(engine.var_tve())
            else: forecasts.append(engine.var_tve_garch())
        
        tester = bt.VaRBacktester(test_returns, np.array(forecasts))
        p_kup, p_obs = tester.kupiec_test()
        summary.append({
            "Methode": m, 
            "Exceptions": tester.x, 
            "Taux_Obs": round(p_obs * 100, 2),
            "P_value_Kupiec": round(p_kup, 4),
            "Statut": "Valide" if p_kup > 0.05 else "Rejete"
        })

    # --- ÉTAPE 4 : REPORTING ---
    df_res = pd.DataFrame(summary)
    print("\n\n[4] Génération des rapports...")
    rp.export_to_excel(df_res)
    rp.generate_pdf(df_res)

    print("\n====================================================")
    print("ANALYSE TERMINÉE")
    print(f"Rapports disponibles dans : {os.path.abspath('outputs')}")
    print("====================================================")

if __name__ == "__main__":
    main()