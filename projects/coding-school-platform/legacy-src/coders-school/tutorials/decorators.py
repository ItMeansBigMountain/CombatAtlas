import functools


'''
THIS CODE WILL CREATE A DECORATOR TO REPEAT CODE A SET AMOUNT OF TIMES, USING THE DECORATOR
'''


# decorator function to repeat a function x amount of times
def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args , **kwargs):
            for x in range(num_times):
                results = func(*args , **kwargs)
            return results
        return wrapper
    return decorator_repeat





# NOTICE HOW THE DECORATOR HAS AN ARGUMENT WHICH IS THE SAME ARGUMENT FOUND ON THE FUNCTION WITH THE SAME NAME.
@repeat(num_times = 4)
def sayHello(x):
    greeting = "hello, {}".format(x)
    return x



results = sayHello('Affan')

print(results)

