from sklearn import svm
from sklearn.externals import joblib
from sklearn import datasets


iris = datasets.load_iris()
digit = datasets.load_digits()

# print(digit.data)
# print(digit.target)

clf = svm.SVC(C=100,gamma=0.001)

clf.fit(digit.data[:-1],digit.target[:-1])

clf.predict(digit.data[-1])

joblib.dump(clf,"model.pkl")

print(clf.score(digit.data[:-1],digit.target[:-1]))
#
# result = clf.predict([2, 2])  # predict the target of testing samples
#
# print(clf.score(X,y))
#
# print (result)  # target
#
# print (clf.support_vectors_)  # support vectors
#
# print (clf.support_)  # indeices of support vectors
#
# print (clf.n_support_)  # number of support vectors for each class