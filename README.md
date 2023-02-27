# assignment 8

## Main purpose
randomly generate 3D creature and evolve it in generations <br>

## Basic idea
### Random generation rule
1. Has a torso of 3*3*1 in the middle, and 4 limbs at each conor
2. Each limb has random link number, link size, and link position (but must connected)
3. Each limb has random distribution of sensor neurons (but total sensro number > 0)
4. Limbs are symetric with repect to y-z plane
5. All joint has motor neurons, all motor nuerons has synpases with all sensor neurons


figure 1. diagram of body and brain generation

### Evolving rule
To mimic the evlovement in nature, body evolvement only happens in every 20 generations,<br>
but brain evolvement and neuron distribution evolvement are happening in every generation. 

1. synapses weight randomly change one in every generation
2. link size randomly change one in every generation
3. link number and link position change every 20 generation



figure 2. diagram of evolve loop

### Fitness setting
Simply set the moving distance at y direction as the fitness<br>


## Result 
By running search.py, you can have result like:
(video: https://youtu.be/D5y4FWz41jY)

And by running plotfitness.py, you can see the fitness curve.
Two typical type of fitness curve is shown as below:

Typical case that one always win:
![Typical case that one always win (best fitness)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case1-bestfintess.png)
![Typical case that one always win (fitness of all population)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case1-fintess.png)


Typical case of fairly competitation:
![Typical case of fairly competitation (best fitness)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case2-bestfintess.png)
![Typical case of fairly competitation (fitness of all population)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case2-fintess.png)
