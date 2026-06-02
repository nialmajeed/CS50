

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
When utilisng the Kernel (top right) and applying it to the big matrix (left) we can summarise the big matrix into a smaller matrix botton right. 

One kernel that is commonly used is :

This is used to find edges in images

Pooling:
Flattening
Dropout: 

Optimisers:
- adam

Loss:
- categorical_crossentropy


Basline:
Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
Max-pooling layer, using 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
Flatten units
        tf.keras.layers.Flatten(),
Add a hidden layer with dropout
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),
    Droupout
    tf.keras.layers.Dropout(0.5),
Add an output layer with output units for all 10 digits
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),

Output:
accuracy: 0.0569 - loss: 3.4980




Test 1 will be based off this input but increasing the Density of the hidden lay from 64, 128 to  256
# Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
# Flatten units
    tf.keras.layers.Flatten(),
# Add a hidden layer with dropout
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.5),
# Add an output layer with output units for all 10 digits
 tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),

Output: accuracy: 0.0553 - loss: 3.4993

Using a desity of:
128: accuracy: 0.0571 - loss: 3.5008
256: accuracy: 0.8002 - loss: 0.7257
512: accuracy: 0.9234 - loss: 0.3268

There is a drastic increase in the accurace and reduction is loss - is this due to the dropout rate. Hence I will see how the dropout rate affects the result for each of the above densities 

Dropout of 0.2: 
64: accuracy 0.0549 - loss: 3.4980
128: accuracy 0.5064 - loss: 1.6500
256: accuracy: 0.9294 - loss: 0.3577
512: accuracy: 0.9374 - loss: 0.4865

Dropout of 0.35:
64: accuracy: 0.2796 - loss: 2.7084
128: accuracy: 0.0552 - loss: 3.5001
256: accuracy: 0.7954 - loss: 0.7307
512: accuracy: 0.9304 - loss: 0.2771

Dropout of 0.5:
64: accuracy: 0.0560 - loss: 3.4952
128: accuracy: 0.0571 - loss: 3.5008
256: accuracy: 0.8002 - loss: 0.7257
512: accuracy: 0.9234 - loss: 0.3268


From these results, it looks like to get the best balance of reduction of loss, increase in accuracy and reduction in cost/time etc. 

As this is a small overview I will simpley take a dropout rate of 0.2 nd desnsity of 256 moving forward as I will now remove max pooling to see the effect:

First thing - the process took much longer and the resuts were sub par.  
0.8633 - loss: 0.5373

with a 2x2 pool we go the following results: 
256: accuracy: 0.9294 - loss: 0.3577
3x3: accuracy: 0.9476 - loss: 0.2510
4x4: accuracy: 0.9327 - loss: 0.2837

From this quick experiment it looks as if 3x3 is the best option as increasing the size of your max pooling will not continuously make your answer more accurate. While a larger pool can summarize a broader area, making it too large destroys critical, fine-grained details, leading to a loss of information and potentially dropping your accuracy


Second wave: 
2x2: accuracy: 0.9123 - loss: 0.3761
3x3: accuracy: 0.8075 - loss: 0.6299

\due to the above, i will not include a secondary pooling. 

Reviewing Convolution filters & Layers: 

1st layer:
32: 0.9476 - loss: 0.2510
64: 0.9399 - loss: 0.3109

Adding a second convlution layer:
32: 0.9506 - loss: 0.2867
64: 0.9743 - loss: 0.1604

third layer:
32: accuracy: 0.9791 - loss: 0.1156
64: accuracy 0.9880 - loss: 0.0750

Taking 3 convlution layers at 64 filter due to the reduction in loss: 

1 hidden layer:
accuracy: 0.9728 - loss: 0.1524

2 hidden layers:
accuracy:0.9524 - loss: 0.2714

3 hidden layers: 
accuracy: 0.9764 - loss: 0.1107

If i did the experiement again, I would have down the convlution laye first and worked down. I would also like to change multiple things at a time rather than doing them one by one. 
I would also like to see the effect  changing the number of filters and sizes per convolution layer as well as changing the density per hidden layer added 
I would also like to look into pooling etc after hidden layers nstead of pooling already pooled sections etc. 
I would also need to trible check each run to ensure no outliers were taken into account.


Final solution looks like this:
    model = tf.keras.models.Sequential(
        [
            # Convolutional layer. Learn 32 filters using a 3x3 kernel
            tf.keras.layers.Conv2D(
                64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
            ),
            tf.keras.layers.Conv2D(
                64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
            ),
            tf.keras.layers.Conv2D(
                64, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
            ),
            # Max-pooling layer, using 2x2 pool size
            # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            # Max-pooling layer, using 2x2 pool size
            tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),
            # tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),
            # Flatten units
            tf.keras.layers.Flatten(),
            # Add a hidden layer with dropout
            # tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            # tf.keras.layers.Dense(256, activation="relu"),
            # Droupout
            tf.keras.layers.Dropout(0.2),
            # Add an output layer with output units for all 10 digits
            tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"),
        ]
    )