# Final Project: Distributed network vs Centralized network (the Scientist)

Octopus has a great control of its limbs, enableing various behavior patterns, which allows it to mimic almost everything in the sea, and attack its prey without being noticed. 
It is believed that the octopus has more than one brain. Actually, it has 9: mini one for each limbs and a main one in the middle. This distributed neuron network might be the
reason why it can be so capabale and flexible.<br>
![diagram1](https://github.com/LJQ434/ME495/blob/final_project/final%20project/octopus%20brain.png)

In this project, we will look into the difference between centeralized neuron network which we are commomly used in all our assignments, and the octopus-like distributed neuron network.
Will they be different? Which one performs better? And why?

## Hypothesis
On the task of moving with limbs, the distributed neuron network performs better than centralized network.

## Method
The hypothesis is examined based on the 3D random quadruped in assignment 8 [click to see detials]()<br>
The body generation and brain structure is as follows:<br>

### body generation
The robot is consists of 4 limbs and 1 torso. 4 limbs are geometrically symetric by x-z plane. <br>
The sensor number is set as constant in each limb to control the variables.<br>
But the limb's shape, size, and sensor distribution is still random and evolvable. <br>
The generation rule is shown in following diagram:<br>

![diagram1](https://github.com/LJQ434/ME495/blob/final_project/final%20project/body%20generation%20diagram.png)<br>
fig 1. diagram of body generation<br>

### brain structure
to compare the centralized and distributed neuron network, we set the experiment group as follows: <br>

Group1: Centralized network without hidden neurons<br>
Group2: Distributed network without hidden neurons<br>
Group3: Centralized network with 8 hidden neurons in the center<br>
Group4: Distributed network with 2 hidden neurons in each limb (total 8)<br>
<br>

The diagram of each groups' neuron networks is shown as below:<br>

![diagram2](https://github.com/LJQ434/ME495/blob/final_project/final%20project/brain%20structure-%20with%20hidden.png)<br>
fig 2. diagram of brain structure<br>

### Evolve and Select
Weigths of synapses and limb's body size is slightly and randomly mutate in every generation.
So the parents will have a similar shape with its children. But the children may be smarter.<br> 

In every 20 genenrations, the limbs' body number and body direction has a large mutation. 
Such mutation will randomly move a body of a limb to a new direction, add or delete a body in a limb.
Children will inherit the basic shape, but different in one limb. Also, it might have more or less motor neurons. <br>

<br> 
the fitness is defined as: y/abs(1+x)<br>
And only the winner with higher fitness can pass its gene to the next genegration.<br>

![diagram3](https://github.com/LJQ434/ME495/blob/final_project/final%20project/evolve%20diagram.png)<br>
fig 3. diagram of evolvement<br>

## Result 
5 runs are conducted independently for each group, 5 initial parents are applied for each run, and each individual experiences 500 generations.<br>
That is, each group has a 5*5*500 = 25000 simulations, which will be sufficient for statistical analysis. <br>
The average fitness and best fitness among all populations in all runs are ploted as below:<br>

![diagram4](https://github.com/LJQ434/ME495/blob/final_project/final%20project/result%20diagram.png)<br>
fig 4. average and best fitness curve of each group<br>
As can be seen in the plots, the average fitness of the distributed brain increase faster than that of the centralized brain with the same neuron number.
And the average curve of distributed brain is always higher than the centralized brain. 
That means the distributed network has a faster training speeed, which might due to the small number of synapses it has compared to the centralized brain.
The less the synapses, the less searching space, and the faster it can find the optimal point.
However, that might also due to the low efficiency of random search. Obviously the centralized network has more possibilities, and thus great potentials that has 
not been fully discovered with random search. <br>
<br>
We can also see from the best fitness curve that the distributed network with hidden neurons is the best. But the distributed network not always performs better than
the centralized one. Centralized network with hidden neurons performs similarly with the distributed network without the hidden neurons. 


And the performance of the best individual of each group can be seen in this video: [video](https://youtu.be/ppdzcMhPtC8) <br>
It can be easily observed from the video that the centralized brain can hardly move its limb seperately, but always move together. 
The distributed brain, however, is good at controling the limbs seperately.
And thus the quadruped with distributed brain can walk or run, but the centralized one can only have small jumps and our creeping.
Running with long legs is always faster than creeping, as it is proved in the real world. 
That might be the second reason that the distributed brain performs better than the centralized brain. 

## Conclusion
*1. On the task of moving forwar, with the body of 3D quadruped, with the same amount of sensor and hidden neurons, the distributed network has faster learning <br>
speed and seperatable limb control, which makes it performs better within the limited 500 generations than the centralized brain. <br>
*2. Adding hidden neurons will improve the performance of quadruped, and the best individua of centralized network quadraped with 8 hidden neurons has similar <br>
performance with the distributed network quadraped, so the distributed brain is not always better.<br>

## Future plan
To further investigate how the distributed neuron network performs, a more complex task should be assigned. For example, <br>
*1. let the robot climb steps or over rugged terrain<br>
*2. Let the robot get through holes like octopus<br>
<br>
And a more hierarchical network should be involved: mini brains for local control and main brains for totoal control.<br>
<br>
The random search method may not serve the purpose well. So a more efficient learning method should be considered and applied.<br>
<br>
## Reference
Ludobots, by DrJosh [reddit link](https://www.reddit.com/r/ludobots/)<br>
Pyrosim adn pybullet[link](https://pybullet.org/wordpress/)<br>
ME495 Artificial Life, teached by [Sam Kriegman](https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/kriegman-sam.html)<br>

## files description 
All .py code should be run under the recommended environment [environment](https://www.reddit.com/r/ludobots/wiki/installation/) <br>
solution.py is different for each group. Other files are the same. <br>
Result data in the above analysis are also provided in each group's folder <br>
Youtube Video: [video](https://youtu.be/ppdzcMhPtC8)<br>

