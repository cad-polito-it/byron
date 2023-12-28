import pytest
from byron.classes.monitor import failure_rate 
from byron.classes.monitor import _STAT  
from byron.user_messages import performance_warning
from functools import wraps



@failure_rate
def conditional_function(condition):
    if condition:
        return True
    else:
        return False



@pytest.mark.parametrize("condition", [True, False])
def test_conditional_function(condition):
    assert conditional_function(condition) == condition


def failure_rate(func):
    """ Generate sporadic RuntimeWarning messages if the failure rate is above 90% """
    @wraps(func)
    def wrapper(*args, **kwargs):
        exception = None
        try:
            result = func(*args, **kwargs)
            print(f"Called {func.__name__}, result: {result}")
        except Exception as e:
            result = False
            exception = e
            print(f"Exception in {func.__name__}: {e}")

        _STAT[(func, bool(result))] += 1
        print(f"Updated _STAT: {_STAT}")

        if not result:
            failures = _STAT[(func, False)]
            successes = _STAT[(func, True)]
            total = failures + successes
            print(f"Failures: {failures}, Successes: {successes}, Total: {total}")
            if failures / total > 0.9 and any(total == 10**n for n in range(2, 10)):
                performance_warning(f"The failure rate of '{func.__qualname__}' is {100 * failures / total:g}% "
                                    f"({successes:,} success{'es' if successes != 1 else ''} out of {total:,} calls)")
        if exception:
            raise exception
        else:
            return result
    return wrapper
