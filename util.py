import numpy as np
import pyproximal
from scipy.optimize import minimize

def generate_test_constraint(m, n=None):
    if n == None:
        n = m
    A = np.random.rand(m, n) * 10
    x = np.arange(1, n+1)
    b = A @ x
    return A, b, x

def f_L1(x):
    return np.sum(np.abs(x))

def grad_L1(x):
    return np.sign(x)
    
def f_affine_L1(x, M):
    return np.sum(np.abs(M @ x))

def grad_affine_L1(x, M):
    return np.sign(M @ x)

def f_quad(x):
    return 0.5 * x.T @ x

def grad_quad(x):
    return x

class MyProx(pyproximal.proximal.Nonlinear):
    def __init__(self, x0, niter=10, warm=True, f=None, g=None):
        super().__init__(x0, niter=10, warm=True)
        self.f = f
        self.grad = g

    def fun(self, x):
        return self.f(x)
    
    def grad(self, x):
        return self.g(x)
    
    def optimize(self):
        def callback(x):
            self.solhist.append(x)
        self.solhist = []
        self.solhist.append(self.x0)
        sol = minimize(lambda x: self._funprox(x, self.tau),
                                   x0=self.x0,
                                   jac=lambda x: self._gradprox(x, self.tau),
                                   method='L-BFGS-B', callback=callback)
        sol = sol.x

        self.solhist = np.array(self.solhist)
        return sol
    
