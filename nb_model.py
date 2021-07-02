from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from pandas import read_csv
import numpy as np


def nb():
    data_path = 'data.csv'
    data_table = read_csv(data_path)
    data_table = data_table.sample(frac=0.25)
    comment = [i for i in data_table['comment_text']]
    is_toxic = np.array([i for i in data_table['toxic']])
    is_toxic.reshape(-1, 1)
    train_comment, test_comment, train_is_toxic, test_is_toxic = train_test_split(comment, is_toxic, test_size=0.2)

    # converting comments into a matrix for the naive bayes function
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.5, sublinear_tf=True)
    train_comment = vectorizer.fit_transform(train_comment)
    test_comment = vectorizer.transform(test_comment)

    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(train_comment, train_is_toxic)
    train_comment = selector.transform(train_comment).toarray()
    test_comment = selector.transform(test_comment).toarray()

    # creating and training the naive bayes model
    model = GaussianNB()
    model.fit(train_comment, train_is_toxic)
    y_pred = model.predict(test_comment)

    matrix = confusion_matrix(test_is_toxic, y_pred)
    print(matrix)
    print(model.score(test_comment, test_is_toxic))


if __name__ == '__main__':
    nb()
