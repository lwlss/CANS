from CANS_functions import *
import pandas as pd

# Timepoints at which we would like to simulate cell densities (& remaining nutrients)
t=np.linspace(0,4.5,100)

nrow,ncol=3,3

# Initial conditions
C0=0.001
N0=0.23

# Parameter value
r=[3,3,3,3,10,3,3,3,3]
k=0.05

# Initial conditions
C=[C0 for x in range(0,nrow*ncol)]
N=[N0 for x in range(0,nrow*ncol)]

# Define function specifying what ODE is
# y is a list of variables (only one variable in this case: C)
# t is a list of times at which we will calculate variables
f=makeModelComp(nrow,ncol,r,k)

soln=odeint(f,C+N,t)

# Read in some real data
data=pd.read_csv("..\data\ColonyzerOutput.txt",sep="\t")

# Plotting results
fig,ax=plt.subplots(nrow,ncol,figsize=(20,10))
for row in range(nrow):
    for col in range(ncol):
        dat=data[(data.Column==(col+1))&(data.Row==(row+1))]
        i=convertij((row+1,col+1),ncol)
        ax[row,col].scatter(dat.ExptTime,dat.Intensity,c="red")
        ax[row,col].plot(t,soln[:,i],c="black")
        ax[row,col].plot(t,soln[:,i+(nrow*ncol)],c="blue")
        ax[row,col].set_ylim([-0.02,0.3])
        ax[row,col].text(4, 0.275, 'R{r:02d}C{c:02d}'.format(r=row+1,c=col+1))
        ax[row,col].set_xlabel('Time since inoculation (d)')
        ax[row,col].set_ylabel('Population size (AU)')
plt.show()

