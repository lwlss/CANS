from CANS_functions import *

# Parameters describing biology/physics of problem
# nrow, ncol: Dimensions of plate array (cells inoculated in rectangular grid pattern)
# rA: Rate at which cells undergo temporary arrest in presence of signal (EthOH)
# rC: Rate at which cells recover from arrests
# rS: Rate at which signal (EthOH) is produced by cells
# kN: Rate of "diffusion" of nutrients between positions
# kS: Rate of "diffusion" of signalling molecules between positions

nrow=16; ncol=24
# Randomly generate some growth rate parameters (genotype specific)
rparams=[random.gauss(4.0,1.0) for x in range(0,nrow*ncol)]
# Timepoints at which we would like to simulate cell densities (& remaining nutrients)
t=np.linspace(0,15,100)

# Initial conditions
C0=0.0001       # Density of dividing cells in inoculum
A0=0            # Density of arrested cells in inoculum
N0=1.0          # Starting nutrient conc. at each position
S0=0.0          # Starting signal conc. at each position
C=[C0 for x in range(0,nrow*ncol)]  # Assume that robot inoculates same number of cells in each position
A=[A0 for x in range(0,nrow*ncol)]  # Assume that no cells in initial population are arrested
N=[N0 for x in range(0,nrow*ncol)]  # Assume that nutrients evenly distributed around plate
S=[0 for x in range(0,nrow*ncol)]   # No signalling molecules (or ethanol) at start of experiment

# Set up model, specifying parameters
f=makeModel(nrow,ncol,rparams,rA=0.1,rC=0.05,rS=0.0,kN=0.1,kS=0.01)

# Simulation
soln=odeint(f,C+A+N+S,t)

# Plotting results
for i in range(0,nrow*ncol):
    plt.plot(t,soln[:,i])
plt.xlabel('Time since inoculation (d)')
plt.ylabel('Population size (AU)')
plt.title('Logistic growth')
plt.show()



