import yfinance as yf
import pandas as pd
import numpy as np

def get_portfolio_data(tickers, start_date, end_date):
    # On télécharge les données
    df = yf.download(tickers, start=start_date, end=end_date)
    
    # Correction pour les nouvelles versions de yfinance :
    # Si 'Adj Close' n'existe pas, on prend 'Close'
    if 'Adj Close' in df.columns:
        data = df['Adj Close']
    elif 'Close' in df.columns:
        data = df['Close']
    else:
        # Cas où yfinance renvoie un MultiIndex (plusieurs tickers)
        # On essaie de chercher 'Adj Close' dans les niveaux de colonnes
        try:
            data = df.xs('Adj Close', axis=1, level=0)
        except:
            data = df.xs('Close', axis=1, level=0)

    # Calcul des log-rendements
    returns = np.log(data / data.shift(1)).dropna()
    
    # Si on a plusieurs colonnes (plusieurs actifs), on fait la moyenne 
    # pour simuler un portefeuille équipondéré
    if isinstance(returns, pd.DataFrame):
        returns = returns.mean(axis=1)
        
    return data, returns