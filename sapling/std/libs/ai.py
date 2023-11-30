from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

from sapling.std.call_decorator import call_decorator
from sapling.objects import Array, Float, Class


class model:
    __name__ = 'model'
    type = 'model'
    
    def __init__(self, dataset: list, labels: list) -> None:
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(dataset, labels, test_size=0.2)
        
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression())
        ])
        
        self.model.fit(self.x_train, self.y_train)

    @staticmethod
    def repr(_) -> str:
        return 'model()'
    
    
    @call_decorator({'input': {'type': 'array'}}, req_vm=False)
    def _predict(self, inp: Array) -> Float:
        y_pred = self.model.predict(self.x_train)
        accuracy = accuracy_score(self.y_test, y_pred)
        return Float(inp.line, inp.column, accuracy)


class ai:
    type = 'ai'

    @call_decorator({'dataset': {'type': 'array'}, 'labels': {'type': 'array'}}, req_vm=False)
    def _train(self, dataset: Array, labels: Array):
        return Class.from_py_cls(model(
            dataset.to_py_list(), labels.to_py_list()
        ), dataset.line, dataset.column)
