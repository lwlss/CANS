from CANS_functions import *

# Timepoints at which we would like to simulate cell densities (& remaining nutrients)
t=np.linspace(0,15,100)

# Initial conditions
C0=0.1
N0=10.0

# Parameter value
r=0.1

# Define function specifying what ODE is
# y is a list of variables (only one variable in this case: C)
# t is a list of times at which we will calculate variables
def f(y,t):
    C=y[0]
    N=y[1]
    # Specify model here
    dC=[r*C*N]
    dN=[-r*C*N]
    return(dC+dN)

iconds=[C0,N0]
soln=odeint(f,[C0,N0],t)

# Plotting results
for i in range(0,2):
    plt.plot(t,soln[:,i])
plt.xlabel('Time since inoculation (d)')
plt.ylabel('Population size (AU)')
plt.title('Logistic growth')
axes = plt.gca()
axes.set_ylim([0,max(soln[:,0])])
plt.show()
