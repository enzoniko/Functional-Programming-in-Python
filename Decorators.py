import time


def time_decorator(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f'{f.__name__} took {end - start} seconds')
        return result
    return wrapper


def debug_decorator(f):
    def wrapper(*args, **kwargs):
        print(f'{f.__name__} called with args: {args}, kwargs: {kwargs}')
        return f(*args, **kwargs)
    return wrapper


def result_decorator(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        print(f'{f.__name__} returned: {result}')
        return result
    return wrapper


def debug_result_time_decorator(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f'{f.__name__} took {end - start} seconds')
        #print(f'{f.__name__} called with args: {args}, kwargs: {kwargs}')
        print(f'{f.__name__} returned: {result}')
        return result
    return wrapper


"""def processable_decorator(f):
    def wrapper(*args, **kwargs):
        for element in args:
            if isinstance(element, dict):
                result = f(*args, **kwargs)
                element[args - element] = result
                return result
    return wrapper"""
