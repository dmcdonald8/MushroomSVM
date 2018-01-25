import numpy as np

class validation_case():
    
    def __init__(self, training_data_size, features, dropnan):
        
        self.training_data_size = training_data_size
        self.features = features
        self.dropnan = dropnan
        self.predictions = []
        self.targets = []
        self.ratios = []
        self.accuracy = 0.0
        
    def add_results(self, predictions, y):
        self.predictions.append(predictions)
        self.targets.append(y)
        
        num_correct = sum(int(a == y) for a, y in zip(predictions, y))
        ratio = float(num_correct) / float(len(y))
        self.ratios.append(ratio)
        self.generate_average_accuracy()
        
    def generate_average_accuracy(self):
        self.accuracy = np.mean(self.ratios)
        return self.accuracy