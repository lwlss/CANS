I had parameters (sub-directory) from a simulation of the competition
model with kn=0 in a 3x3 plate. Starting with uniform r estimates, of
r_i = 1, this was fit well by the independent model but poorly by the
competition model (see data in sub-directory).

In an attempt to fix this I used independent estimates as the starting
point for competition fits.

I made competition simulations varying kn from 0-0.2 by increments of
0.02 and keeping other parameters the same.

This suceeds at kn up to 1.2. Above this value the independent
solution is a local minimum.

Next I will try several random sets of starting rs.

times = np.linspace(0, 20, 201)
kns = np.linspace(0, 0.2, 11)

Initial guesses:
Inde:
C(t=0), N(t=0), r_i
[0.005, 0.8, 1.0]

Comp:
Inde estimates with kn=0

Stopping criteria:
Default
