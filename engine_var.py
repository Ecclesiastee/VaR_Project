import numpy as np
from scipy.stats import norm, skew, kurtosis, genpareto
from arch import arch_model

class VaREngine:
    def __init__(self, returns, confidence_level=0.95):
        self.returns = returns
        self.alpha = 1 - confidence_level
        self.mean = np.mean(returns)
        self.std = np.std(returns)

    def var_historical(self):
        return -np.percentile(self.returns, self.alpha * 100)

    def var_parametric(self):
        return -(self.mean + norm.ppf(self.alpha) * self.std)

    def var_cornish_fisher(self):
        s, k, z = skew(self.returns), kurtosis(self.returns), norm.ppf(self.alpha)
        z_cf = (z + (z**2 - 1) * s / 6 + (z**3 - 3*z) * k / 24 - (2*z**3 - 5*z) * s**2 / 36)
        return -(self.mean + z_cf * self.std)

    def var_riskmetrics(self, lam=0.94):
        vols = np.zeros(len(self.returns))
        vols[0] = self.std
        for t in range(1, len(self.returns)):
            vols[t] = np.sqrt(lam * vols[t-1]**2 + (1 - lam) * self.returns.iloc[t-1]**2)
        return -(self.mean + norm.ppf(self.alpha) * vols[-1])

    def var_garch(self):
        model = arch_model(self.returns, vol='Garch', p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        next_vol = np.sqrt(res.forecast(horizon=1).variance.values[-1, -1])
        return -(self.mean + norm.ppf(self.alpha) * next_vol)

    def var_tve(self):
        losses = -self.returns
        threshold = np.percentile(losses, 90)
        exceedances = losses[losses > threshold] - threshold
        shape, loc, scale = genpareto.fit(exceedances)
        n, n_u = len(losses), len(exceedances)
        return threshold + (scale / shape) * (((self.alpha * n / n_u)**(-shape)) - 1)

    def var_tve_garch(self):
        model = arch_model(self.returns, vol='Garch', p=1, q=1, rescale=False)
        res = model.fit(disp='off')
        std_resid = (res.resid / res.conditional_volatility).dropna()
        # TVE sur résidus
        threshold = np.percentile(-std_resid, 90)
        exceedances = -std_resid[-std_resid > threshold] - threshold
        shape, loc, scale = genpareto.fit(exceedances)
        var_resid = threshold + (scale / shape) * (((self.alpha * len(std_resid) / len(exceedances))**(-shape)) - 1)
        next_vol = np.sqrt(res.forecast(horizon=1).variance.values[-1, -1])
        return var_resid * next_vol