import sys
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

def load_data(messages_filepath, categories_filepath):
    """
    Takes in a csv file and outputs a merged pandas Dataframe
    INPUT -
    messages_filepath: filepath for messages
    categories_filepath: filepath for categories
    OUTPUT - 
    df - Merged dataframe
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories, on='id')
    return df


def clean_data(df):
    """
    Intakes merged dataframe, cleans, and removes duplicates from the dataframe
    
    INPUT - df: Uncleaned Dataframe
    OUTPUT - df: Cleaned Dataframe
    """
    categories = df.categories.str.split(pat=';',expand=True)
    row = categories.iloc[0,:]
    category_colnames = row.apply(lambda x: x[:-2])
    categories.columns = category_colnames
    for column in categories:
    # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
    
    # convert column from string to numeric
        categories[column] = categories[column].astype(np.int)
    df.drop('categories',axis=1, inplace=True)
    df = pd.concat([df,categories],axis=1)
    # Check duplicates
    print("There are {} duplicates out of {} items in dataset".format(df.duplicated().sum(),df.shape[0]))
    df.drop_duplicates(inplace=True)
    # Check duplicates again
    print("There are {} duplicates out of {} items in dataset".format(df.duplicated().sum(),df.shape[0]))
    return df


def save_data(df, database_filepath):
    """
    Save the dataframe to a SQLite database
    INPUT - 
    df: Cleaned dataframe
    database_filepath: Filepath for SQLite Database
    OUTPUT - Saved SQLite database
    """
    engine = create_engine('sqlite:///'+database_filepath)
    df.to_sql('Disaster', engine, index=False)


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
