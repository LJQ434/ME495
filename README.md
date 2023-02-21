#### assignment 7

### main purpose:

extend random body generation algorism to generate random 3D body. 


### method:

    ## body structure description:
        
        To make the shape of the 3D random creature more concise and beautiful, I decided to apply symmetricity to it. In this example case, body structure is shown in figure with below link:

        (body strucure diagram link: https://drive.google.com/file/d/14OCK8fjFfMWT5NtFPzd0-ivyJ-RVvCaH/view?usp=sharing)

        2 independent limbs are generated separately twice through a linear method, just like random snake, but in 3D. The body number, body size, and the relative position between two neighbor bodies are set random. Motor neurons are set to every joint, but sensor neurons are deployed randomly. All links with sensor neurons are painted ‘Green’. Default color are ‘Cyan’. 

    ## ‘Gene’ construction:

        To make the shape mutable, we need a seed, or you can call it ‘Gene’, to store sufficient information of the shape feature, so that the shape can be rebuild anytime and mutated during the evolvement. 
        The feature includes: the limb number, the size and position of each links in each limbs, the orientation of each joint, and the distribution of sensor neurons. I set the limb number as constant for an individual during the evolvement, to avoid missing of local optimal point.  And in this case I also announced the maximum link number of each limb:
        self.limbnumber = 2
        self.maxlimbbodynumber = 4

        Then I use chromosomes to store the information in each limb:
        self.chromosome_bodysize  
        self.chromosome_bodydirection
        self.chromosome_sonsor

        chromosome_bodysize is a float array of (limbnumber, 3*maxlimbbodynumber), where the 3 position stores x,y,z length of each link. 
        chromosome_bodydirection is a int array of (limbnumber, 3*maxlimbbodynumber), where the 3 positon is -1, 0, or 1, indicates the link’s relative position based on previous link. For example: (0,-1,1) mean new link is on the left bottom of the previous link.
        self.chromosome_sonsor is a int array of (limbnumber, maxlimbbodynumber), where it stores 0 or 1. 0 means no sensor on that link, 1 means having a sensor neuron. The neuron network is generated according to this chromosome. 

    

### Result:
 
By running search.py in the github, you should have somethink like this:
https://drive.google.com/file/d/1Z_xv_6SmZkeFZMTq_ucbOXGYOpvTMm27/view?usp=sharing


### Reference: Luddobots
 

 
