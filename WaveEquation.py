#Modelling of the wave equation

from manim import *

class WavePlotter(Scene):

    def construct(self):
        dt              = 0.1    #Time increments
        t               = 0
        T               = 12     #Total time to run for
        L               = 1      #Length of string
        c               = 1      #Not used in this problem
        N               = 20     #Number of terms used in infinite sum
        g               = -1   #Body force
        scalingFactorH  = 10     #Horizontal scaling factor: affects display but not calculations. Change if string is too short or too long on screen
        scalingFactorV  = 1.5    #Vertical scaling factor: same as above.

        #Example 2 parameters
        # k = 2.4
        # a = 1.6

        
        #Function that calculates u(x,t)
        def u(x):
            uSoln = (g/2)*(x**2 -x)
            for n in range(1,N+1):
                
                '''Ignore these; these are from previous questions'''
                #f(x)=x, g(x)=0
                # uSoln +=  (-2* L/ (n * np.pi)  ) * np.power(-1, n) * np.cos(c* n* np.pi * t /L) * np.sin(n * np.pi * x/L)
                
                #f(x) as pointed function, g(x) = 0
                # p = a
                # q = -a*L/k

                # d = -a
                # e = a*(k-1)*L/k

                # uSoln += np.piecewise(x, [0<=x<(L/k), (L/k)<=x<(L/2), (L/2)<=x<(  (k-1)*L  / k  ), (  (k-1)*L  / k  )<=x<L], 
                #                       [0,
                #                        (2/(n*np.pi)) *    (q - (p*L+q)* (np.power(-1,n))) * np.cos(c* n* np.pi * t /L) * np.sin(n * np.pi * x/L),
                #                        (2/(n*np.pi)) *    (e - (d*L+e)* (np.power(-1,n))) * np.cos(c* n* np.pi * t /L) * np.sin(n * np.pi * x/L),
                #                        0])

                '''The actual question'''
                #Sum over odd terms
                if (n%2)!=0:
                    A_n = (2/ (n*np.pi))* np.sin((n*np.pi)/2)
                    B_n = 4*g /(  n**3 + np.pi**3  )
                    

                    uSoln += A_n * np.sin(n*np.pi*x) * np.sin(n*np.pi*t) + B_n*np.sin(n*np.pi*x) * np.cos(n *np.pi *t)
            
            result= np.array((x*scalingFactorH, uSoln*scalingFactorV, 0))
            return result
        
        #Add label that describes solution plotted
        label = Tex(r"Wave equation $u(x,t)$ with Dirichlet boundary conditions, $u(x,0)=0$, and $u_t(x,0)=\delta(x-\frac{1}{2})$ on $0<x<1$", font_size=33, color=TEAL).shift(3.5*UP)
        self.add(label)    
           
        #Use a parametric function that is parametized in terms of points along the line in the interval [0,L]
        func_i = ParametricFunction(u, t_range = np.array((0, L)), fill_opacity=0).set_color(PURPLE).shift((L*scalingFactorH/2)*LEFT)
        self.add(func_i)
        self.wait(1.5)

        #Iterate and display solution
        while t<T:
            t = t +dt
        
            func_i1 = ParametricFunction(u, t_range = np.array((0, L)), fill_opacity=0).set_color(PURPLE).shift((L*scalingFactorH/2)*LEFT)
            
            self.play(ReplacementTransform(func_i, func_i1, run_time=dt, rate_func=linear))
            func_i = func_i1
        
        self.wait(1.5)
        