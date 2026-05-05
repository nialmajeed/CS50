

The document outlines the considerations, tests and outcomes of different Neural Networks created with the goal of recognising different German traffic lights. 

The Key considerations we will take into account in the model are: 
- No. of Convolution layers (number of layers and sizes of filters)
- No. of Pooling Layers (different sizes of pooling lkayers)
- Number and Size of Hidden layers
- Unit Dropout 


We will create a baseline model which incoperates all of the above specfied features and then further test each one individually to see the positive or negative affects it has on the accuracy and Loss. Then we will attempt to take this information to build am optimised model. 

We will also attempt to utilise th best optimizer, loss functions to gain th most accurate result. 

Accuracy: The proportion of correct predictions out of the total number of predictions made (Evalusation)
Loss: A numerical value representing the error between predicted and actual output (Optimisation)


Other Operations to consider: 
Convoltion: Image convolution is applying a filter that adds each pixel value of an image to its neighbors, weighted according to a kernel matrix. Doing so alters the image and can help the neural network process it.

![alt text](https://github.com/nialmajeed/CS50/blob/d4ded90a51409dcca27db5a1055de7f4a1557c06/L5/traffic/convolution.png "Convolution example")


Pooling:
Flattening
Dropout: 

Optimisers:
- adam

Loss:
- categorical_crossentropy
