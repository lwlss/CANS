import numpy as np
import random
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.interpolate import splrep, splev
import scipy.optimize as opt

def logistic(x0,r,K,t):
    '''Vectorised logistic model'''
    return(K*x0*np.exp(np.multiply(r,t))/(K+x0*(np.exp(np.multiply(r,t))-1)))

def logistic_rhs(r,K,x):
    '''RHS of ode version of logistic model'''
    return(np.multiply(np.multiply(r,x),1-np.divide(x,K)))

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

def makeGradientObjective(t,x,k=5,s=0.01):
    # Fit spline to the data to smooth them
    splinepts = splrep(sim.t_exp,sim.x_obs,k=k,s=s)
    slopes=np.maximum(0,splev(sim.t_exp,splinepts,der=1))
    def obj(p):
        x0,r,K=p
        return(np.sum(np.power(slopes-logistic_rhs(r,K,x),2)))
    return(obj)

def makeODEObjective(t,x):
    def obj(p):
        x0,r,K=p
        return(np.sum(np.power(x-logisticode(x0,r,K,t),2)))
    return(obj)
    

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

sim=sim(x0=0.001,r=5.5,K=0.6,tau=1500.0,v=1.0,n_exp=20)

# Fit spline to the data to smooth them
splinepts = splrep(sim.t_exp,sim.x_obs,k=5,s=0.01)
slopes=np.maximum(0,splev(sim.t_exp,splinepts,der=1))

plt.plot(sim.t_exp,sim.x_obs,label="data")
t_curve=np.linspace(0,max(sim.t_exp),100)

plt.plot(t_curve, splev(t_curve,splinepts), label="fitted")
plt.xlabel("Time since inoculation (d)")
plt.ylabel("Population size (AU)")
plt.show()

# Fit logistic model to data
ODE=makeODEObjective(sim.t_exp,sim.x_exp)
Grad=makeGradientObjective(sim.t_exp,sim.x_exp)

ODE_est = opt.minimize(ODE, [0.001,2,1])
Grad_est = opt.minimize(Grad, [0.001,2,1])

