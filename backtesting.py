import numpy as np
from scipy.stats import chi2

class VaRBacktester:
    def __init__(self, actual_returns, forecast_var, alpha=0.05):
        self.hits = (actual_returns < -forecast_var).astype(int)
        self.n, self.x, self.p = len(self.hits), np.sum(self.hits), alpha

    def kupiec_test(self):
        p_obs = self.x / self.n
        if p_obs in [0, 1]: return 1.0, p_obs
        lr = -2 * ((self.n-self.x)*np.log(1-self.p) + self.x*np.log(self.p) - ((self.n-self.x)*np.log(1-p_obs) + self.x*np.log(p_obs)))
        return 1 - chi2.cdf(lr, df=1), p_obs

    def christoffersen_test(self):
        t00 = t01 = t10 = t11 = 0
        for i in range(1, len(self.hits)):
            if self.hits[i-1]==0 and self.hits[i]==0: t00+=1
            elif self.hits[i-1]==0 and self.hits[i]==1: t01+=1
            elif self.hits[i-1]==1 and self.hits[i]==0: t10+=1
            else: t11+=1
        p01, p11 = t01/(t00+t01), t11/(t10+t11)
        p_all = (t01+t11)/self.n
        lr = -2 * ((self.n-t01-t11)*np.log(1-p_all) + (t01+t11)*np.log(p_all) - (t00*np.log(1-p01)+t01*np.log(p01)+t10*np.log(1-p11)+t11*np.log(p11)))
        return 1 - chi2.cdf(lr, df=1)