import sys
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import precision_recall_fscore_support
import nltk
nltk.download(['punkt','wordnet','averaged_perceptron_tagger'])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
import pickle

def load_data(database_filepath):
    """
    Load SQLite database and return parsed out messages and categories
    INPUT - database_filepath: Filepath for SQLite Database
    OUTPUT - 
    X: Messages to train and predict
    Y: Categories
    category_names: Names of category columns
    """
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('Disaster',engine)
    X = df['message']
    Y = df.iloc[:,4:]
    category_names = Y.columns
    return X, Y, category_names


def tokenize(text):
    """
    Tokenizer for all url types
    """
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens
class StartingVerbExtractor(BaseEstimator, TransformerMixin):

    def starting_verb(self, text):
        """
        Transformer which uses NLP to pick out the first verb in a sentence thorough the parts of speech library in the Natural Language Toolkit.
        INPUT - text: A set of text you wish to analyze
        OUTPUT - True or False depending on if it is the first verb or not.
        """
        sentence_list = nltk.sent_tokenize(text)
        for sentence in sentence_list:
            pos_tags = nltk.pos_tag(tokenize(sentence))
            first_word, first_tag = pos_tags[0]
            if first_tag in ['VB', 'VBP'] or first_word == 'RT':
                return True
        return False

    def fit(self, x, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.starting_verb)
        return pd.DataFrame(X_tagged)

def build_model():
    """
    Build ML Pipeline and run GridSearchCV to optimize model
    OUTPUT - cv: optimized ML Model
    """
    model = Pipeline([
        ('features', FeatureUnion([

            ('text_pipeline', Pipeline([
                ('vect', CountVectorizer(tokenizer=tokenize)),
                ('tfidf', TfidfTransformer())
            ])),

            ('starting_verb', StartingVerbExtractor())
        ])),

        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
    ])
    print('Running Grid Search to find optimized model!')
    parameters = {'clf__estimator__n_estimators':[10,50,100]}
    cv = GridSearchCV(model, param_grid=parameters)
                  
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    """
    Evaluate ML model and return results
    INPUT -
    model: Optimized ML Model
    X_test: Test set of messages
    Y_test: Test set of categories
    category_names: Column names for dataframe
    """
    y_pred = model.predict(X_test)
    results_df = pd.DataFrame(columns=['Category','F1_Score','Precision','Recall'])
    i = 0
    for column in Y_test.columns:
        precision, recall, f1_score, support = precision_recall_fscore_support(Y_test[column], y_pred[:,i],average='weighted')
        results_df.at[i,'Category'] = column
        results_df.at[i,'F1_Score'] = f1_score
        results_df.at[i,'Precision'] = precision
        results_df.at[i,'Recall'] = recall
        i+=1
    print('The average f1_score is: {}'.format(results_df['F1_Score'].mean()))
    print('The average precision is: {}'.format(results_df['Precision'].mean()))
    print('The average recall is: {}'.format(results_df['Recall'].mean()))
    


def save_model(model, model_filepath):
    """
    Save model as a pickle file
    INPUT - 
    model: Optimized ML Model
    model_filepath: Filepath where model is saved
    """
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
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
