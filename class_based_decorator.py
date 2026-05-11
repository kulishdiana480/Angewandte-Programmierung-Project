from icecream import ic


############################################
### Simple function decorator
############################################


def log_decorator(func):
    """Simple decorator that logs function calls"""
    def wrapper(*args, **kwargs):
        ic(f"Calling function: {func.__name__}")
        ic(f"Arguments: {args}, {kwargs}")
        result = func(*args, **kwargs)
        ic(f"Result: {result}")
        return result
    return wrapper


############################################
### Class-based decorator
############################################


class TimerDecorator:
    """Class-based decorator that measures execution time"""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        import time
        start = time.time()
        ic(f"Starting: {self.func.__name__}")
        result = self.func(*args, **kwargs)
        end = time.time()
        ic(f"Finished: {self.func.__name__} in {end - start:.4f} seconds")
        return result


class LogDecorator:
    """Class-based decorator that logs function calls"""

    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        ic(f"Function '{self.func.__name__}' was called")
        ic(f"With args: {args}")
        ic(f"With kwargs: {kwargs}")
        result = self.func(*args, **kwargs)
        ic(f"Returned: {result}")
        return result


############################################
### Example functions with decorators
############################################


@log_decorator
def add_numbers(a: int, b: int) -> int:
    """Simple addition"""
    return a + b


@TimerDecorator
def calculate_square(n: int) -> int:
    """Calculate square of a number"""
    return n * n


@LogDecorator
def greet(name: str) -> str:
    """Greet a person"""
    return f"Hello, {name}!"


@TimerDecorator
@LogDecorator
def slow_function(n: int) -> int:
    """Simulate a slow function"""
    import time
    time.sleep(0.1)
    return n * 2


############################################
### Main
############################################


if __name__ == "__main__":
    print("=== Function Decorator ===")
    result1 = add_numbers(3, 5)
    print(f"Result: {result1}\n")

    print("=== Timer Decorator ===")
    result2 = calculate_square(7)
    print(f"Result: {result2}\n")

    print("=== Log Decorator ===")
    result3 = greet("Diana")
    print(f"Result: {result3}\n")

    print("=== Combined Decorators ===")
    result4 = slow_function(10)
    print(f"Result: {result4}\n")