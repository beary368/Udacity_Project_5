
# Udacity Data Scientist Nanodegree Project 5

## Disaster Response Pipelines

This project utilizes ETL (Extract, Transform, Load), NLP (Natural Language Processing), and ML (Machine Learning) pipelines in order to process tweets/texts during natural disasters.

# Packages

You will need to download a few packages from the Natural Language Tool Kit (nltk). But first you will have to import nltk.
* nltk==3.4
Specifically downloads are below:

```bash
nltk.download(['punkt','wordnet','averaged_perceptron_tagger'])
```
* Numpy==1.15.4
* pandas==0.22.0
* scikit-learn==0.20.1
    * See this website for dependent packages to install [Sklearn](https://github.com/scikit-learn/scikit-learn/blob/master/README.rst#user-installation)
* SQLAlchemy==1.3.1
You will also need to import regex...
```bash
import re
```

# Files

There are 3 folders each containing pieces of the project and a README.

### app

- run.py: app and user interface used to predict results.
- templates: folder containing the html templates

### data

- process_data.py: reads in, cleans, and stores the data in an SQL database (DisasterResponse.db).
- disaster_categories.csv and disaster_messages.csv: These are the two datasets...
- DisasterResponse.db: This is the output database containing the cleaned and transformed data.

### models

- train_classifer.py: Loads the database, transforms the database via NLP, and runs a machine learning model (using a ML Pipeline).

# Authors, Licensing, & Acknowledgements

Wanted to thank [Figure Eight](https://visit.figure-eight.com/better-machine-learning-models.html?source=Paid&medium=GoogleAd&campaign=Branded&content=Demo&term=figure8&matchtype=e&gclid=CjwKCAjwsIbpBRBNEiwAZF8-zx8Jn49P6at_Gl4j9-4wgtRtHnYfJ_uLJQfP6YxjhsYXOqn3U9J2kBoCjI0QAvD_BwE) for providing the dataset for us to analyze.

Wanted to thank [Udacity](https://www.udacity.com/) for providing a platform for me to explore these data sets for an interesting project.
