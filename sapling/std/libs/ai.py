from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

from sapling.std.call_decorator import call_decorator
from sapling.objects import Array, Class, Float
from sapling.error import STypeError


class Model:
    type = 'Model'
    
    def repr(self, _) -> str:
        return f'Model({self.model})'
    
    def __init__(self, model: MultinomialNB, X_test, y_test):
        self.model = model
        
        self.X_test = X_test
        self.y_test = y_test
    
    
    @call_decorator()
    def _test(self, vm) -> Float:
        y_pred = self.model.predict(self.X_test)
        return Float(*vm.loose_pos, accuracy_score(self.y_test, y_pred))


class ai:
    type = 'ai'
    
    @call_decorator({'data': {'type': 'array'}, 'labels': {'type': 'array'}}, is_attr=False)
    def _train(vm, data: Array, labels: Array) -> Class:
        if len(data) != len(labels):
            vm.error(STypeError('data and labels must have the same length', vm.loose_pos))
        
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(data.to_py_list())
        y = LabelEncoder().fit_transform(labels.to_py_list())
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = MultinomialNB()
        model.fit(X_train, y_train)
        return Class.from_py_cls(Model(model, X_test, y_test), data.line, data.column)
