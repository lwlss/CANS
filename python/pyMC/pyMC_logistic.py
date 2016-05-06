import numpy as np
import pymc as mc
import diagnostics as dg
import random
from pymc.Matplot import plot
from scipy.integrate import odeint

def logistic(x0,r,K,t):
    '''Vectorised logistic model'''
    return(K*x0*np.exp(r*t)/(K+x0*(np.exp(r*t)-1)))

# To convert from N-C competition model to logistic model, think about matching rates at t=0
# Competition:
# dC/dt @t0 = rc*C0*N0
# Logistic
# dC/dt @t0 = rl*C0*(1-C0/K)
# In order for growth curves to be identical:
# rc*C0*N0 = rl*C0*(1-C0/K)
# -> rc = rl*(1-C0/K)/N0
# Also need same population size at steady-state:
# Logistic carrying capacity is initial pop size plus increase from nutrient consumption
# K=C0+N0
# -> N0=K-C0
# Therefore:
# rc = rl*(1-C0/K)/(K-C0)
# -> rc = rl/K

def logisticode(x0,r,K,t):
    '''Set of ODEs equivalent to logistic model. Population consumes nutrients, self-limiting when nutrients exhausted.'''
    rc = r/K
    # Define function specifying ODE
    # y: list of species values (C first, then N)
    # t: list of times at which we will calculate variables
    def f(y,t):
        C,N=y
        dC=rc*C*N
        dN=-rc*C*N
        return([dC,dN])
    iconds=[x0,K-x0]
    res=odeint(f,iconds,t)
    # Return C results only, to match logistic output
    return(res[:,0])

class par:
    '''Prior parameters (ranges for uniform distributions)'''
    r_min,r_max=0.0,10.0
    K_min,K_max=0.0,1.0
    x0_min,x0_max=0.0,0.1
    tau_min,tau_max=0,1500000
    v_min,v_max=0.1,10.0

# Simulate some observation times and experimental data, with measurement error
class sim():
    rnd=np.random
    '''Parameters used for generating simulated data, together with simulated data'''
    def __init__(self,x0=0.001,r=2.5,K=0.6,tau=300.0,v=1.0,tmax=5,n_exp=10,n_pred=10):
        self.seed = random.randint(0,4294967295)
        self.K_true=K
        self.r_true=r
        self.x0_true=x0
        self.tau_true=tau
        self.t_exp=np.linspace(0,tmax,n_exp)
        self.t_pred=np.linspace(0,tmax,n_pred)
        self.x_exp=logistic(self.x0_true,self.r_true,self.K_true,self.t_exp)
        self.rnd.seed(self.seed)
        self.x_obs=self.rnd.normal(self.x_exp,np.sqrt(1.0/self.tau_true))

sim=sim()

x0=mc.Uniform('x0',par.x0_min,par.x0_max)
r=mc.Uniform('r',par.r_min,par.r_max)
K=mc.Uniform('K',par.K_min,par.K_max)
tau=mc.Uniform('tau',par.tau_min,par.tau_max)

logfun=logistic
@mc.deterministic(plot=False)
def logisticobs(x0=x0,r=r,K=K):
    return(logfun(x0,r,K,sim.t_exp))
@mc.deterministic(plot=False)
def logisticpred(x0=x0,r=r,K=K):
    return(logfun(x0,r,K,sim.t_pred))

pred=mc.Normal('pred',mu=logisticpred,tau=tau)
obs=mc.Normal('obs',mu=logisticobs,tau=tau,value=sim.x_obs,observed=True)
M=mc.MCMC(dict({"x0":x0,"r":r,"K":K,"tau":tau,"pred":pred,"obs":obs}))
M.sample(iter=250000, burn=1000, thin=100,progress_bar=False)

dg.posteriorPriorPlots(M,sim,par)

