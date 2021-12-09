'''Function for creating and saving classification report. 
'''

from sklearn.metrics import classification_report
import pandas as pd

def evaluate_model(labels, predictions, filename):
    """Create and save classification report
    Args: 
        labels: labels 
        predictions: model predictions
    Returns:
        clf_report: classification report
    """
    # create clf report 
    clf_report = classification_report(labels, predictions)
    
    # create df for storing metrics
    df = pd.DataFrame(classification_report(labels,predictions,output_dict = True)).round(decimals=2)
        
    # save classification report    
    df.to_csv((f"{filename}.csv"), index = True)
    return clf_report
    