"""
This python file is used to define utils that can be used in other files
"""
def error_handler(func):
    """
        A decorator created to handle exceptions for all the calls

        Parameters
        ----------
        func : func, optional
           input func to which decorator is added

        Returns
        -------
        Function
    """
    def Inner_Function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError:
            print(f"{func.__name__} wrong data types. enter numeric")
    return Inner_Function