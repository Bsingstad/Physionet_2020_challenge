#!/usr/bin/env python

import numpy as np
#import joblib
from get_12ECG_features import get_12ECG_features
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential,Model,load_model
from keras.optimizers import Adam, SGD
from scipy.io import loadmat
from keras.layers import Dense, LSTM, Dropout, TimeDistributed, Bidirectional, InputLayer, Flatten, Conv1D, MaxPooling1D, BatchNormalization



def run_12ECG_classifier(data,header_data,classes,model):
    threshold = 0.6

    #num_classes = len(classes)
    #current_label = np.zeros(num_classes, dtype=int)
    #current_score = np.zeros(num_classes)

    # Use your classifier here to obtain a label and score for each class. 
    data12lead = data
    testdata = pad_sequences(data12lead, maxlen=10000, truncating='post',padding="post")
    #features=np.asarray(get_12ECG_features(data,header_data))
    #feats_reshape = features.reshape(1,-1)
    reshaped12lead = testdata.reshape(1,10000,12)
    #label = model.predict(reshaped12lead).T
    score = model.predict_proba(reshaped12lead)
    #current_label[label-2] = 1
    #max_pred_val =np.array([score[0].max(),score[1].max(),score[2].max(),score[3].max(),score[4].max(),score[5].max(),score[6].max(),score[7].max(), score[8].max()])
    score = score.ravel()
    binary_prediction = []
    for i in range(len(score)):
        if (score[i] > threshold):
            binary_prediction.append(1)
        elif (score[i] < threshold):
            binary_prediction.append(0)
    binary_prediction = np.asarray(binary_prediction)

    #for i in range(num_classes):
    #    current_score[i] = np.array(score[0][i])

    #return current_label, current_score
    return binary_prediction, score


def load_12ECG_model():
    # load the model from disk


    model = Sequential()
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu',input_shape=(10000,12),use_bias=True))
    model.add(MaxPooling1D(pool_size=5, stride=3,data_format="channels_last"))
    model.add(BatchNormalization())
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu', use_bias=True))
    model.add(MaxPooling1D(pool_size=5, stride = 3, data_format="channels_last" ))
    model.add(BatchNormalization())
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu', use_bias=True))
    model.add(MaxPooling1D(pool_size=5, stride = 3, data_format="channels_last" ))
    model.add(BatchNormalization())
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu', use_bias=True))
    model.add(MaxPooling1D(pool_size=5, stride = 3, data_format="channels_last" ))
    model.add(BatchNormalization())
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu', use_bias=True))
    model.add(MaxPooling1D(pool_size=5, stride = 3, data_format="channels_last" ))
    model.add(BatchNormalization())
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu', use_bias=True))
    model.add(MaxPooling1D(pool_size=5, stride = 3, data_format="channels_last" ))
    model.add(BatchNormalization())
    model.add(Conv1D(filters=512, kernel_size=5, activation='relu', use_bias=True))
    model.add(MaxPooling1D(pool_size=3, stride = 1, data_format="channels_last" ))
    model.add(BatchNormalization())
    model.add(LSTM(512))
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(9, activation='sigmoid'))
    #model.add(Dense(9, activation='softmax'))


    model.load_weights("weights_best.hdf5")

    model.compile(loss='categorical_crossentropy', optimizer="SGD", metrics=['categorical_accuracy', 'categorical_crossentropy'])


    return model
