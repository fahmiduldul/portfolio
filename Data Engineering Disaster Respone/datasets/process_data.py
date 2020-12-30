import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

'''
run this file from root folder:
python3 datasets/process_data.py datasets/messages.csv datasets/categories.csv datasets/DisasterResponse.db
'''

def load_data(messages_filepath, categories_filepath):
    """
    PARAMETER:
    messages_filepath - filepath for messages
    categories_filepath - filepath for categories

    RETURN:
    df - merged messages and categories DataFrame
    """

    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)

    df = pd.concat([messages, categories], axis=1)

    return df

def clean_data(df):
    '''
    PARAMETER:
    df (DataFrame) - dataframe to be cleaned

    RETURN:
    df (DataFrame) - cleaned dataframe
    '''
    #split categories from one column to 36 columns
    categories = df['categories'].str.split(';', expand=True)

    #get columns name for each categories and set it to categories df
    category_colnames = categories.iloc[1] \
        .apply(lambda x: x[0:-2])
    categories.columns = category_colnames

    #convert categories value to 0 and 1
    for column in categories:
        categories[column] = categories[column].str[-1]
        categories[column] = pd.to_numeric(categories[column])
    
    # merge categories df into master df
    df = pd.concat([df.drop(['id','categories'], axis=1), categories], axis=1)

    # remove duplicates
    df = df[~df.duplicated()]

    #check for non-binary result
    nonbinary_cols = []
    for category in df.drop(columns=['message', 'original', 'genre']).columns:
        if len(list(df[category].unique())) > 2:
            nonbinary_cols.append(category)

    # convert non 0 and 1 to 1
    for category in nonbinary_cols:
        df[category][~df[category].isin([0,1])] = 1

    return df

def save_data(df, database_filename):
    '''
    PARAMETER:
    df (DataFrame) - dataframe to be saved
    database_filename (string) - database file name

    RETURN:
    None
    '''
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('messages_and_categories', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
            .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
            'datasets as the first and second argument respectively, as '\
            'well as the filepath of the database to save the cleaned data '\
            'to as the third argument. \n\nExample: python process_data.py '\
            'disaster_messages.csv disaster_categories.csv '\
            'DisasterResponse.db')


if __name__ == '__main__':
    main()