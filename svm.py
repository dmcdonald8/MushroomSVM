import svm_loader
from sklearn import svm
import pandas as pd
import numpy as np
import validation_cases as vc

# Global variable for the size of the training data as a percentage of the 
# whole dataset. Validation and test data will be half the remaining data each
training_data_size = 0.8
training_data, validation_data, test_data = svm_loader.load_data(training_data_size)

# Global variable for number of case features to use in model
features = 18

# Global variable to determine whether to drop cases with NaN values
# If set to false the it will inpute the missing value with the mean column value
dropnan = True
#Global variable for the Support Vector Classifier model
model = svm.SVC(kernel="linear", C = 1.0)

def reload_data():
    global training_data_size, training_data, validation_data, test_data
    training_data, validation_data, test_data = svm_loader.load_data(training_data_size)
    
# Function for handling NaN values in a subset of the data
def pre_process(dataset):
    global features, dropnan
    # Create a new subset of features and their classes so that NaN values
    # can be dropped or inputed only when they occur in this subset
    sample_data = dataset.iloc[:, : features]
    sample_target = dataset.iloc[:, -1]
    samples = pd.concat([sample_data, sample_target], axis=1)
    
    # Drop NaN values or inpute with mean depending on global variable
    if (dropnan):
        samples.dropna(inplace=True)
        
    else:
        samples.fillna(samples.mean(),inplace=True)
    
     # Get sample dataset
    X = samples.iloc[:, : -1]
    
    # Get Class column as target for classification of samples
    y = samples.iloc[:, -1 ]
    
    return X, y

# Method for training the model using the training dataset
def train():
    global model, training_data, features

    X, y = pre_process(training_data)

    print "Building module..."
    model.fit(X, y)
    print "Building complete"
    
    training_predictions = [int(a) for a in model.predict(X)]
    
    num_correct = sum(int(a == y) for a, y in zip(training_predictions, y))
    print "%s of %s values correct." % (num_correct, len(y))
    ratio_correct = float(num_correct) / float(len(y))
    print "Ratio correct: %s" % (ratio_correct)
    
    return training_predictions, y

# Method for testing the trained model after using the test dataset
def test():
    global model, validation_data, features
    X, y = pre_process(test_data)

    test_predictions = [int(a) for a in model.predict(X)]
    
    num_correct = sum(int(a == y) for a, y in zip(test_predictions, y))
    print "%s of %s values correct." % (num_correct, len(X))
    ratio_correct = float(num_correct) / float(len(X))
    print "Ratio correct: %s" % (ratio_correct)
    
    return test_predictions, y, ratio_correct

# Method for tuning the model using validation data by changing the variables
# used and recording the outcome. It then sets the optimal variables from this
def validate():
    global training_data_size, features, dropnan, model
    
    # Initialise global variables to lowest desired
    training_data_size = 0.5
    features = 10
    validation_cases = []
    while (training_data_size < 0.9):
        
        #Reload data to be used with new variable set
        reload_data()
        print "\nTraining data size: " + str(training_data_size)
        while (features <= 21):
            print "Features: " + str(features)
            train()
            X, y = pre_process(validation_data)
            
            # Create a new validation case from output of prediction
            validation_case = vc.validation_case(training_data_size,
                                                 features, dropnan)
            validation_predictions = [int(a) for a in model.predict(X)]
            validation_case.add_results(validation_predictions, y)
            print "Dropnan True: \n Accuracy: " + str(validation_case.accuracy)
            
            # Appoend to validation cases for analysis later
            validation_cases.append(validation_case)
            
            #Toggle dropnan
            dropnan = False
            X, y = pre_process(validation_data)
            validation_case = vc.validation_case(training_data_size,
                                                 features, dropnan)
            validation_predictions = [int(a) for a in model.predict(X)]
            validation_case.add_results(validation_predictions, y)
            print "Dropnan False: \n Accuracy: " + str(validation_case.accuracy)
            validation_cases.append(validation_case)
            
            features += 1
            dropnan = True
            
        features = 10 
        training_data_size += 0.05
  
    # initialise validation case    
    best_validation = vc.validation_case(0.0, 0, True)
    
    # Find the case with the highest accuracy
    for case in validation_cases:
        if case.accuracy > best_validation.accuracy:
            best_validation = case
            
    print "\nBest validation case: "
    print "Training data size: " + str(best_validation.training_data_size)
    print "Features used: " +str(best_validation.features)
    print "Drop NaN?: " + str(best_validation.dropnan)
    print "Accuracy: " + str(best_validation.accuracy) 
    print "Setting these as variables for testing"
    training_data_size = best_validation.training_data_size
    features = best_validation.features
    dropnan = best_validation.dropnan
    
    # Reload data with optimum size
    reload_data()
    
# Analyses confusion in results for confusion matrix
def confusion(predictions, y):
    # False positives and negatives + True positives and negatives
    TP, TN, FP, FN = 0, 0, 0, 0
    
    for x, y in zip(predictions, y):
        #True positive
        if (x == 1 and y == 1):
            TP += 1      
        # True negative
        if (x == 0 and y == 0):
            TN +=1
        # False positive
        if (x == 1 and y == 0):
            FP += 1
        # False negative
        if (x == 0 and y == 1):
            FN += 1
            
    print "True Positive: " + str(TP)
    print "True Negative: " + str(TN)
    print "False Positive: " + str(FP)
    print "False Negative: " +str(FN)
    
    return TP, TN, FP, FN

def run():
    train()
    reload_data()
    validate()
    train()
    test()
    
    average_accuracy = []
    test_number = 50
    print "\nRunning %s tests...." % (test_number)
    for i in range(test_number):
        reload_data()
        train()
        predictions, y, accuracy = test()
        average_accuracy.append(accuracy)
    print "Tests complete"
    print "Average accuracy: " + str(np.mean(average_accuracy))
    
    print "Confusion statistics for last test: "
    confusion(predictions, y)

run()
    
  

    
    