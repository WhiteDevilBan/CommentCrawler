import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from site.mybzz.sentiment import feature_selection


def text_classifly_twang(dataset_dir_name, fs_method, fs_num):
    print('Loading dataset, 80% for training, 20% for testing...')
    movie_reviews = load_files(dataset_dir_name)
    doc_str_list_train, doc_str_list_test, doc_class_list_train, doc_class_list_test = train_test_split(
        movie_reviews.data, movie_reviews.target, test_size=0.2, random_state=0)

    print('Feature selection...')
    print('fs method:' + fs_method, 'fs num:' + str(fs_num))

    vectorizer = CountVectorizer(binary=True)
    word_tokenizer = vectorizer.build_tokenizer()
    doc_terms_list_train = [word_tokenizer(doc_str) for doc_str in doc_str_list_train]
    term_set_fs = feature_selection.feature_selection(doc_terms_list_train, doc_class_list_train, fs_method)[:fs_num]

    print
    'Building VSM model...'
    term_dict = dict(zip(term_set_fs, range(len(term_set_fs))))
    vectorizer.fixed_vocabulary = True
    vectorizer.vocabulary_ = term_dict
    doc_train_vec = vectorizer.fit_transform(doc_str_list_train)
    doc_test_vec = vectorizer.transform(doc_str_list_test)

    clf = MultinomialNB().fit(doc_train_vec, doc_class_list_train)  # 调用MultinomialNB分类器
    doc_test_predicted = clf.predict(doc_test_vec)

    acc = np.mean(doc_test_predicted == doc_class_list_test)
    print
    'Accuracy: ', acc

    return acc


if __name__ == '__main__':
    dataset_dir_name = "E:\MyProject\python\comment\site\mybzz\sentiment"
    fs_method_list = ['IG', 'MI', 'WLLR']
    fs_num_list = range(25000, 35000, 1000)
    acc_dict = {}

    for fs_method in fs_method_list:
        acc_list = []
        for fs_num in fs_num_list:
            acc = text_classifly_twang(dataset_dir_name, fs_method, fs_num)
            acc_list.append(acc)
        acc_dict[fs_method] = acc_list
        print
        'fs method:', acc_dict[fs_method]

    for fs_method in fs_method_list:
        plt.plot(fs_num_list, acc_dict[fs_method], '--^', label=fs_method)
        plt.title('feature  selection')
        plt.xlabel('fs num')
        plt.ylabel('accuracy')
        plt.ylim((0.82, 0.86))

    plt.legend(loc='upper left', numpoints=1)
    plt.show()