1) Make a grid of 1000 (or more) C_0 values from 10e-3 to 10e-?  Fix
   at the plate level by supplying as a bound to logistic model
   guessing.  Run on yzer and use 50 cores.  1000/50 = 20 full plate
   fits per core.  Slice values for each script as C_0[i:i+20] so that
   even if only the first fits run for each we have a resolution of 100.

2) I don't think that b guesses are required if C_0 is fixed.

3) Make sure to save N_0 for EACH CULTURE and THE TOTAL OF the
objective function for each fit. Also save objective function for each
culture.

4) Make sure to create the correct directories in yzer and run using a
bash script.

5) Handle runtime errors as general exceptions
