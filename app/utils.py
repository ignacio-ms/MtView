import time


def timed(fun):
    """
    Function to time a especific function.
    """

    def wrapper(*args, **kwargs):
        before = time.time()
        res = fun(*args, **kwargs)
        after = time.time()

        f_name = fun.__name__
        print(f'{f_name} took {after - before}[s] to execute.\n')
        return res
    return wrapper


def update_progress(progress):
    """
    Function to print a progress bar of a given percentage.
    """

    print(f"\r [{'#' * (progress // 10)}{' ' * (10 - (progress // 10))}] {progress}%", end='')
