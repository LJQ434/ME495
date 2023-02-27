# assignment 8

## Main purpose
randomly generate 3D creature and evolve it in generations <br>

## Basic idea
### Random generate body and brain
1. Has a torso of 3x3x1 in the middle, and 4 limbs at each conor<br>
2. Each limb has random link number, link size, and link position (but must connected)<br>
3. Each limb has random distribution of sensor neurons (but total sensro number > 0)<br>
4. Limbs are symetric with repect to y-z plane<br>
5. All joint has motor neurons, all motor nuerons has synpases with all sensor neurons<br>

![diagram of body and brain generation](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/body%20structure%20diagram.png)<br>

### Evolving rule
To mimic the evlovement in nature, body evolvement only happens in every 20 generations,<br>
but brain evolvement and neuron distribution evolvement are happening in every generation. 

1. synapses weight randomly change one in every generation<br>
2. link size randomly change one in every generation<br>
3. link number and link position change every 20 generation<br>

![diagram of evolve loop](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/evolve.png)<br>


### Fitness setting
Simply set the moving distance at y direction as the fitness<br>


## Result 
By running search.py, you can have result like:<br>
(video: https://youtu.be/D5y4FWz41jY)

And by running plotfitness.py, you can see the fitness curve.<br>
Two typical type of fitness curve is shown as below:<br>

Typical case that one always win:<br>
![Typical case that one always win (best fitness)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case1-bestfintess.png)
![Typical case that one always win (fitness of all population)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case1-fintess.png)


Typical case of fairly competitation:<br>
![Typical case of fairly competitation (best fitness)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case2-bestfintess.png)
![Typical case of fairly competitation (fitness of all population)](https://github.com/LJQ434/ME495/blob/3D-crab-evolve/Case2-fintess.png)

## Reference
1. [Ludobots](https://www.reddit.com/r/ludobots/) <br>
