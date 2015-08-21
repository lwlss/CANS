from CANS_functions import *

# Timepoints at which we would like to simulate cell densities (& remaining nutrients)
t=np.linspace(0,15,100)

# Initial condition
C0=0.1

# Parameter value
r=0.1

# Define function specifying what ODE is
# y is a list of variables (only one variable in this case: C)
# t is a list of times at which we will calculate variables
def f(y,t):
    C=y[0]
    # Specify model here
    dC=[r*C]
    return(dC)

iconds=[C0]
soln=odeint(f,iconds,t)

# Plotting results
plt.plot(t,soln)
plt.xlabel('Time since inoculation (d)')
plt.ylabel('Population size (AU)')
plt.title('Logistic growth')
axes = plt.gca()
axes.set_ylim([0,max(soln)])
plt.show()
