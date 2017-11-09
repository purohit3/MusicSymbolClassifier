# Music Symbol Classifier

This repository is the model trainer part of the Music Symbol Classifier, which classifies handwritten Music Symbols into 32 different classes using Deep Learning and the HOMUS dataset of handwritten music symbols. It is part of a set of three tools:

|[Model Trainer](https://github.com/apacha/MusicSymbolClassifier)|[Mobile App](https://github.com/apacha/MobileMusicSymbolClassifier)|[Manual Classifier](https://github.com/apacha/ManualMusicSymbolClassifier)|
|:----:|:-----:|:-----:|
|Trains a deep network to automatically classify images of handwritten music symbols into 32 different classes.|Mobile Android application that uses a trained model to perform real-time classification on a mobile device.|A small C#/WPF application that can be used manually classify images, used during evaluation|
|[![Build Status](https://travis-ci.org/apacha/MusicSymbolClassifier.svg?branch=master)](https://travis-ci.org/apacha/MusicSymbolClassifier)|TBD|[![Build status](https://ci.appveyor.com/api/projects/status/2lxb6eg6qnfj9jq5?svg=true)](https://ci.appveyor.com/project/apacha/manualmusicsymbolclassifier)|
|[![codecov](https://codecov.io/gh/apacha/MusicSymbolClassifier/branch/master/graph/badge.svg)](https://codecov.io/gh/apacha/MusicSymbolClassifier) [![Code Health](https://landscape.io/github/apacha/MusicSymbolClassifier/master/landscape.svg?style=flat)](https://landscape.io/github/apacha/MusicSymbolClassifier/master)|||

Note my previous project which classifies images into Music scores or something else which can be found in [this](https://github.com/apacha/MusicScoreClassifier) repository on Github.

An extensive overview of the results of different parameters is documented in this [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1D9kHRhrOBogcrr5ko1DleCnHVKGGNkwbBc6_mnfA6XE/edit?usp=sharing)


# Running the application
This repository contains several scripts that can be used independently of each other. 
Before running them, make sure that you have the necessary requirements installed. 

## Requirements

- Python 3.6
- Keras 2.0.6
- Tensorflow 1.2.1 (or optionally tensorflow-gpu 1.2.1)

Optional: If you want to print the graph of the model being trained, install GraphViz on Windows via http://www.graphviz.org/Download_windows.php and add /bin to the PATH or run `sudo apt-get install graphviz` on Ubuntu (see https://github.com/fchollet/keras/issues/3210)

For installing Tensorflow and Keras we recommend using [Anaconda](https://www.continuum.io/downloads) or 
[Miniconda](https://conda.io/miniconda.html) as Python distribution (we did so for preparing Travis-CI and it worked).

To accelerate training even further, you can make use of your GPU, by installing tensorflow-gpu instead of tensorflow
via pip (note that you can only have one of them) and the required Nvidia drivers. For Windows, we recommend the
[excellent tutorial by Phil Ferriere](https://github.com/philferriere/dlwin). For Linux, we recommend using the
 official tutorials by [Tensorflow](https://www.tensorflow.org/install/) and [Keras](https://keras.io/#installation).

## Training the model

Run `python ModelTrainer/TrainModel.py` or `ModelTrainer/TrainBestModel.ps1` for automatically training a neural network with the best available configuration. It will automatically download and extract the HOMUS dataset.

The result of this training is a .h5 (e.g. res_net_4.h5) file that contains the trained model and when running via the PowerShell-script a transcript of the entire training is also created for later investigation.

`TrainModel.py` has a couple of parameters that can be changed for the training. Note that all options have meaningful default values, so they are completely optional:

- `--dataset_directory` the folder where the images should be stored. Default is `data`
- `--datasets` Specifies which datasets are used for the training. One or multiple datasets of the following are possible: homus, rebelo1, rebelo2, printed, audiveris, muscima_pp, fornes or openomr. Multiple values are connected by a separating comma, i.e. `homus,rebelo1`.
- `--use_existing_dataset_directory` Whether to delete and recreate the dataset-directory (by downloading the appropriate files from the internet, extracting and generating images) or simply use whatever data currently is inside of that directory. This flag should not be provided, if you switch datasets.
- `--model_name` the name of the model configuration used for training (e.g. `vgg4`). Run `ListAvailableConfigurations.ps1` or `models/ConfigurationFactory.py` to get a list of all available configurations
- `--width` Width of the input-images for the network in pixel
- `--height` Height of the input-images for the network in pixel

Further parameters for optional hyperparameter tuning

- `--minibatch_size` Size of the minibatches for training, typically one of 8, 16, 32, 64 or 128
- `--optimizer` The optimizer used for the training, can be SGD, Adam or Adadelta
- `--no_dynamic_learning_rate_reduction` True, if the learning rate should not be scheduled to be reduced on a plateau
- `--class_weights_balancing_method` The optional weight balancing method for handling unbalanced datasets. If provided, valid choices are simple or skBalance. 'simple' uses 1/sqrt(#samples_per_class) as weights for samples from each class to compensate for classes that are underrepresented. 'skBalance' uses the Python SkLearn module to calculate more sophisticated weights.



# License

Published under MIT License,

Copyright (c) 2017 [Alexander Pacha](http://alexanderpacha.com), [TU Wien](https://www.ims.tuwien.ac.at/people/alexander-pacha)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
