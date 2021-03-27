'''
to run this file from app/ directory:
python3 train_classifier.py database/DisasterResponse.db models/test_model.pickle test
the "test" argument used to run the model with only 100 messages
'''

import sys

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlite3 as sq
import re
import pickle
from tabulate import tabulate
from tokenizer import tokenize

import nltk
nltk.download(['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger'])
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import f1_score

def load_data(database_filepath):
    '''
    PARAMETER:
    database_filepath (string) - database directory

    RETURN:
    X (DataFrame) - X DataFrame
    Y (DataFrame) - Y DataFrame
    category_names (string[]) - array of category names
    '''
    df = pd.read_sql("SELECT * FROM messages_and_categories", sq.connect(database_filepath))

    if sys.argv[-1] == "test":
        df = df.iloc[:20]

    X = df["message"]
    Y = df.drop(["message", "original", "genre"], axis=1)
    category_names = Y.columns

    return (X, Y, category_names)


def build_model():
    '''
    PARAMETER:
    None

    RETURN:
    model (GridSearchCV) - grid search model
    '''
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])

    parameters = {
        'clf__estimator__n_estimators': [50,100],
        'clf__estimator__min_samples_split': [2, 4],
    }

    return GridSearchCV(pipeline, param_grid=parameters)


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    PARAMETER:
    model (BaseEstimator) - trained model
    X_test (DataFrame) - X test Dataframe
    Y_test (DataFrame) - Y test Dataframe
    category_names (string[]) - array of category name

    RETURN:
    None
    '''
    Y_preds = pd.DataFrame(model.predict(X_test), columns=category_names)

    headers = ['category', 'precision', 'recall', 'f1-score', 'support']
    rows = []
    for category in category_names:
        report = classification_report(Y_test[category], Y_preds[category], output_dict=True)
        rows.append([
            category,
            report['weighted avg']['precision'],
            report['weighted avg']['recall'],
            report['weighted avg']['f1-score'],
            report['weighted avg']['support']
        ])
    
    print(tabulate(rows, headers=headers) )


def save_model(model, model_filepath):
    '''
    PARAMETER:
    model (BaseEstimator) - trained model
    model_filepath (string) - save file directory

    RETURN:
    None
    '''
    with open(model_filepath, 'wb') as dir:
        pickle.dump(model.best_estimator_, dir)


def main():
    if len(sys.argv) == 4:
        database_filepath, model_filepath = sys.argv[1:3]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
            'as the first argument and the filepath of the pickle file to '\
            'save the model to as the second argument. \n\nExample: python '\
            'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()