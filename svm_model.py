from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from pandas import read_csv
import numpy as np


def svm():
    data_path = 'data.csv'
    data_table = read_csv(data_path)
    data_table = data_table.sample(frac=0.01)
    comment = [i for i in data_table['comment_text']]
    is_toxic = np.array([i for i in data_table['toxic']])
    is_toxic.reshape(-1, 1)
    train_comment, test_comment, train_is_toxic, test_is_toxic = train_test_split(comment, is_toxic, test_size=0.2)

    # converting comments into a matrix for svm
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.5, sublinear_tf=True)
    train_comment = vectorizer.fit_transform(train_comment)
    test_comment = vectorizer.transform(test_comment)

    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(train_comment, train_is_toxic)
    train_comment = selector.transform(train_comment).toarray()
    test_comment = selector.transform(test_comment).toarray()

    # creating and training the svc model
    model = SVC(gamma='scale')
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    scores = cross_val_score(model, test_comment, test_is_toxic, scoring='roc_auc', cv=cv, n_jobs=-1)
    print(np.mean(scores))
    # returned mean score of 0.85


def weighted_svm():
    data_path = 'jigsaw-toxic-comment-classification-challenge/train.csv/train.csv'
    data_table = read_csv(data_path)
    data_table = data_table.sample(frac=0.10)
    comment = [i for i in data_table['comment_text']]
    is_toxic = np.array([i for i in data_table['toxic']])
    is_toxic.reshape(-1, 1)
    train_comment, test_comment, train_is_toxic, test_is_toxic = train_test_split(comment, is_toxic, test_size=0.2)

    # converting comments into a matrix for svm
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.5, sublinear_tf=True)
    train_comment = vectorizer.fit_transform(train_comment)
    test_comment = vectorizer.transform(test_comment)

    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(train_comment, train_is_toxic)
    train_comment = selector.transform(train_comment).toarray()
    test_comment = selector.transform(test_comment).toarray()

    # creating and training the svc model
    model = SVC(gamma='scale', class_weight={0: 1.0, 1: 9.4})
    model.fit(train_comment, train_is_toxic)
    y_pred = model.predict(test_comment)
    y_pred = [round(value) for value in y_pred]
    matrix = confusion_matrix(test_is_toxic, y_pred)
    print(f'confusion matrix: {matrix}')
    print(model.score(test_comment, test_is_toxic))


if __name__ == '__main__':
    weighted_svm()
