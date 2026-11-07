from functools import wraps

def my_decoration(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Prepare the pizza base...")
        result = func(*args, **kwargs)
        print("Adding extra toppings before serving!")
        return result

    return wrapper