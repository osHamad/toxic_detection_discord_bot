from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from pandas import read_csv
import numpy as np
from xgboost import XGBClassifier
import pickle


def xgb():
    # opening data file from disk into read mode
    data_path = 'data.csv'
    data_table = read_csv(data_path)

    # sampling data
    data_table = data_table.sample(frac=0.75)
    print('data sampled')

    # splitting data
    comments = [i for i in data_table['comment_text']]
    is_toxic = np.array([i for i in data_table['toxic']]).reshape(-1, 1)
    train_comment, test_comment, train_is_toxic, test_is_toxic = train_test_split(comments, is_toxic, test_size=0.3)
    print('data split')

    # converting comments into a matrix for XGB
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.6, sublinear_tf=True)
    train_comment = vectorizer.fit_transform(train_comment)
    test_comment = vectorizer.transform(test_comment)
    print('data vectorized')

    # converting label array into required shape for model
    train_is_toxic = train_is_toxic.ravel()
    test_is_toxic = test_is_toxic.ravel()

    # creating and training the XGB model
    print('training model')
    model = XGBClassifier(learning_rate=0.5, scale_pos_weight=12.5)
    model.fit(train_comment, train_is_toxic)
    print('model trained')

    # printing score of model
    model_score = model.score(test_comment, test_is_toxic)
    print(model_score)

    # printing false negative and false positive rates of model
    y_pred = model.predict(test_comment)
    y_pred = [round(value) for value in y_pred]
    matrix = confusion_matrix(test_is_toxic, y_pred)
    print(matrix[0][1] / (matrix[0][1] + matrix[0][0]))
    print(matrix[1][0] / (matrix[1][0] + matrix[1][1]))

    pickle.dump(model, open('xgb_model.sav', 'wb'))
    pickle.dump(vectorizer, open('vectorizer.sav', 'wb'))


if __name__ == '__main__':
    xgb()
