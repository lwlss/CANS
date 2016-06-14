"""Write ODE's in Stan format."""
import pystan

# Practice with SHO
# write stan model
sho_code = """
functions {
    real[] sho(real t,
               real[] y,
               real[] theta,
               real[] x_r,
               int[] x_i) {
        real dydt[2];
        dydt[1] <- y[2];
        dydt[2] <- -y[1] - theta[1] * y[2];
        return dydt;
    }
}
data {
    int<lower=1> T;
    real y[T, 2];
    real t0;
    real ts[T];
}
transformed data {
    real x_r[0];
    int x_i[0];
}
parameters {
    real y0[2];
    vector<lower=0>[2] sigma;
    real theta[1];
}
model {
    real y_hat[T, 2];
    sigma ~ cauchy(0, 2.5);
    theta ~ normal(0, 1);
    y0 ~ normal(0, 1);
    y_hat <- integrate_ode(sho, y0, t0, ts, theta, x_r, x_i);
    for (t in 1:T) {
        y[t] ~ normal(y_hat[t], sigma);
    }
}
"""


# Simulate noisy observations, y_hat:
# function sho,
# initial state, y0
# initial time, t0
# requested solution times, ts
# parameters theta,
# real data x_r,
# integer data x_i
y_hat <- integrate_ode(sho, y0, t0, ts, theta, x_r, x_i);
# Measurement error is then added using normal_rng.

# Stan can infer unknown initial states and/or parameters. The ODE
# solver is used deterministically to produce predictions.
