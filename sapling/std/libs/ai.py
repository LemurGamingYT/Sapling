from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

from sapling.std.call_decorator import call_decorator
from sapling.objects import Array, Float, Class


class model:
    __name__ = 'model'
    type = 'model'
    
    def __init__(self, dataset: list, labels: list) -> None:
        self.cv = CountVectorizer()
        features = self.cv.fit_transform(dataset)
        
        features_train, self.features_test, labels_train, self.labels_test = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )
        
        self.model = MultinomialNB()
        self.model.fit(features_train, labels_train)
        

    @staticmethod
    def repr(_) -> str:
        return 'model()'
    
    
    @call_decorator({'input': {'type': 'array'}}, req_vm=False)
    def _predict(self, inp: Array) -> Float:
        return Float(inp.line, inp.column, accuracy_score(
            self.labels_test,
            self.model.predict(self.features_test),
        ))


class ai:
    type = 'ai'

    @call_decorator({'dataset': {'type': 'array'}, 'labels': {'type': 'array'}}, req_vm=False)
    def _train(self, dataset: Array, labels: Array):
        return Class.from_py_cls(model(
            dataset.to_py_list(), labels.to_py_list()
        ), dataset.line, dataset.column)
