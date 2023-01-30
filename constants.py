import numpy
import constants as c

numberOfGenerations=10
populationSize = 3

iter=1000 #iteration times
am={}
f={}
p={}
F={}

#backleg
am[0] = 1*numpy.pi/4         # amplitude of backleg
f[0] = 2*numpy.pi/iter*10    # frequency of backleg
p[0] = 0                     # phaseOffset of backleg
F[0] = 28                    # maxForce of backleg

#frontleg
am[1] = -1*numpy.pi/4         #amplitude of front
f[1] = 4*numpy.pi/iter*10    #frequency of frontleg
p[1] = 0                     #phaseOffset of frontleg
F[1] = 28                    #phaseOffset of backleg