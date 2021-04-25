def greetings(func):
    def wrapper(*args):
        words = [x.capitalize() for x in func(*args).split()]
        return f'Hello {" ".join(words)}'
    return wrapper

def is_palindrome(func):
    def wrapper(*args):
        txt = ''
        for x in func(*args):
            if x.isalnum():
                txt+=x.lower()
        print(txt)
        if txt == txt[::-1]:
            return f'{func(*args)} - is palindrome'
        else:
            return f'{func(*args)} - is not palindrome'
    return wrapper

def format_output(*strings):
    def format(func):
        def wrapper(*args, **kwargs):
            dict = func()
            keys = [arg for arg in strings]
            print(keys)
            newDict = {arg: '' for arg in strings}
            values = []
            for x in keys:
                if '__' in x:
                    newKeys = x.split('__')
                    for key in newKeys:
                        if key not in dict:
                            raise ValueError
                        values.append(dict[key])
                        newDict[x] = ' '.join(values)
                else:
                    if x not in dict:
                        raise ValueError
                    else:
                        newDict[x] = dict[x]
            return newDict
        return wrapper
    return format

class A:
    pass

def add_class_method(A):
    def wrapper(func):
        @classmethod
        def newFunc(cls):
            return func()
        setattr(A, func.__name__, newFunc)
        return func
    return wrapper

def add_instance_method(A):
    def wrapper(func):
        def newFunc(self):
            return func()
        setattr(A, func.__name__, newFunc)
        return func
    return wrapper