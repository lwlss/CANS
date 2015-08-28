from CANS_functions import *

# Timepoints at which we would like to simulate cell densities (& remaining nutrients)
t=np.linspace(0,15,100)

nrow,ncol=3,3

# Initial conditions
C0=0.1
N0=0.05

# Parameter value
r=[0.1,0.2,0.3,0.2,0.1,0.15,0.15,0.5,0.4]
#r=[0.3 for x in range(0,nrow*ncol)]
k=0.01

# Initial conditions
C=[C0 for x in range(0,nrow*ncol)]
N=[N0 for x in range(0,nrow*ncol)]

# Define function specifying what ODE is
# y is a list of variables (only one variable in this case: C)
# t is a list of times at which we will calculate variables
f=makeModelComp(nrow,ncol,r,k)

soln=odeint(f,C+N,t)

# Plotting results
fig,ax=plt.subplots(nrow,ncol,figsize=(20,10))
for row in range(nrow):
    for col in range(ncol):
        i=convertij((row,col),ncol)
        ax[row,col].plot(t,soln[:,i])
        ax[row,col].set_xlabel('Time since inoculation (d)')
        ax[row,col].set_ylabel('Population size (AU)')
plt.show()

