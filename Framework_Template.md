# Basics ideas to describe a framework
下面是一个模板来对于每个框架的参数进行基本的解释和认识。

## used Libs

## core problem:
 - supervised/unsupervised
 - classification/clustering/regression
 - generation 

## suggested Network type:
 - CNN
 - RNN
 - GAN
 - classical ML

## datasets type 
 - image,text,sound,video,..?
 - fixed size or floating size?
 - series or single item?

## input data shape
 - image: (batch_size,channels,rows,cols)
 - text: (batch_size,tokenized_dim,..)

## target label/data type
 - image: generated image/classification label
 - text: generated text/classification label
 
## preprocessing:
 - text: tokenize, onehot label
 - image: image crop/random flip flop/padding into same dim
 - basics: shuffle size/shuffle time
 - train/test split size

## network related:
 - dropout:
 - each layer: padding, kernel, stride, input/output channel
 - activation function:

## hyper parameters:
 - Batch size:
 - epochs:
 - learning rate decay:
 - regularizers:

## model related:
 - save checkpoint
 - loss: crossentropy/mse/variantes of cross-entropy(binary,sparse,..)
 - optimizer: sgd/adam/adagrad
 - learning rate
 - metrics: accuracy/val_accuracy (for evaluation)
 - training device: cpu/cuda

## methods against overfitting/underfitting:
 - functions in callbacks: earlystopping/