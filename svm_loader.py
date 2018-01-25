import pandas as pd
import convert_csv
import os.path

def load_data(training_size):
    if (not os.path.isfile('mushroom-numerical.csv')):
        print "if statement"
        converter = convert_csv.Converter()
        converter.generate_numerical_csv()
        
    df = pd.read_csv('mushroom-numerical.csv')

    # Shuffle the data and reset the index
    df = df.sample(frac=1).reset_index(drop=True)

    rows = len(df.index)

    validation_idx = int(round(rows * training_size))

    diff = ((1 - training_size) / 2)
    test_idx = int(round(rows * (training_size + diff)))
    
    training_data = df.iloc[ : validation_idx]

    validation_data = df.iloc[ validation_idx : test_idx ]

    test_data = df.iloc[ test_idx : ]

    return training_data, validation_data, test_data
    
