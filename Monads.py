# Libraries
from collections.abc import Callable
from typing import Dict
import traceback
from Decorators import *
from multiprocessing import Process, Manager
from fast_map import fast_map_async

# Maybe Monad


class MaybeMonad:

    # Constructor, receives a value and a flag if the monad contains a value or not
    def __init__(self, value: object = None, contains_value: bool = True):
        # Value of the monad
        self.value = value
        # Flag if the monad contains a value or not
        self.contains_value = contains_value
        # Id of the monad
        self.id = id(self)

    # Bind method, receives a function and applies it to the value of the monad
    def bind(self, f: Callable) -> 'MaybeMonad':
        # If the monad doesn't contain a value, return a monad with no value
        if not self.contains_value:
            return MaybeMonad(None, contains_value=False)
        # Otherwise, return a monad with the value of the function applied to the value of the monad
        try:
            result = f(self.value)
            return MaybeMonad(result)
        # If an error occurs, return a monad with no value
        except Exception:
            return MaybeMonad(None, contains_value=False)


# Failure Monad
class FailureMonad:

    # Constructor, receives a value and a dictionary with the error status of the monad
    def __init__(self, value: object = None, error_status: Dict = None):

        # Value of the monad
        self.value = value
        # Dictionary with the error status of the monad
        self.error_status = error_status
        # Id of the monad
        self.id = id(self)

    # Bind method, receives a function and applies it to the value of the monad with other arguments and keyword arguments
    def bind(self, f: Callable, *args, **kwargs) -> 'FailureMonad':

        # If the error status of the monad is not empty, return a monad with no value
        if self.error_status:
            return FailureMonad(None, error_status=self.error_status)

        # Otherwise, return a monad with the value of the function applied to the value of the monad with other arguments and keyword arguments
        try:
            result = f(self.value, *args, **kwargs)
            return FailureMonad(result)

        # If an error occurs, return a monad with no value and creates an error status
        except Exception as e:

            failure_status = {
                'trace': traceback.format_exc(),
                'exc': e,
                'args': args,
                'kwargs': kwargs
            }

            return FailureMonad(None, error_status=failure_status)

    # Consecutive_binds method, receives a function or a functions list and applies each function to a list of arguments
    def consecutive_binds(self, f, *args, **kwargs) -> 'FailureMonad':

        # If the error status of the monad is not empty, return a monad with no value
        if self.error_status:
            return FailureMonad(None, error_status=self.error_status)

        # Otherwise
        try:
            # If consecutive_binds received a function or a functions list with only one function
            if isinstance(f, Callable) or (isinstance(f, list) and len(f) == 1 and isinstance(f[0], Callable)):
                # If it is a functions list with only one function
                if isinstance(f, list) and len(f) == 1 and isinstance(f[0], Callable):
                    # takes the function out of the list
                    f = f[0]

                # If there is only one argument and it isn't a list
                if len(args) == 1 and not isinstance(args[0], list):

                    # Binds the function to the argument
                    return self.bind(f, *args, **kwargs)

                # If there is only one argument and it is a list
                elif len(args) == 1 and isinstance(args[0], list):

                    # Binds the function to the first argument of the list
                    last = self.bind(f, args[0][0], **kwargs)

                    # Binds the function to the other arguments of the list
                    for i in range(1, len(args[0])):
                        last = last.bind(f, args[0][i], **kwargs)

                    # Returns the bound monad
                    return last

                # If there aren't any arguments binds the function to the value of the monad
                elif len(args) == 0:
                    return self.bind(f, **kwargs)

                # If there are more than one argument
                else:

                    # Binds the function to the first argument
                    last = self.bind(f, args[0], **kwargs)

                    # Binds the function to the other arguments
                    for i in range(1, len(args)):
                        last = last.bind(f, args[i], **kwargs)

                    # Returns the bound monad
                    return last

            # If consecutive_binds received a functions list and there is an arguments list with the same length of the functions list - 1
            elif isinstance(f, list) and len(args) == 1 and isinstance(args[0], list) and len(f) == len(args[0]) + 1:

                # Binds the first function to the first argument of the list
                last = self.bind(
                    f[0], args[0][0], **kwargs)

                # Binds the other functions to the other arguments of the list
                for i in range(1, len(args[0])):
                    last = last.bind(f[i], args[0][i], **kwargs)

                # Returns the bound monad
                return last

            # Otherwise, raise an exception because the arguments are invalid
            else:
                raise Exception('Invalid arguments')

        # If an error occurs, return a monad with no value and creates an error status
        except Exception as e:

            failure_status = {
                'trace': traceback.format_exc(),
                'exc': e,
                'args': args,
                'kwargs': kwargs
            }

            return FailureMonad(None, error_status=failure_status)

# ParallelFailureMonadsPool


class ParallelFailureMonadsPool:
    # Constructor, receives a list of arguments and a list of functions
    def __init__(self, arguments, functions):
        self.arguments = arguments
        self.functions = functions
        self.results = []

    # On_result method
    def on_result(self, x):
        self.results.append(str(x)[:10]) if x is not None and not isinstance(
            x, dict) else self.results.append(x)

    @ debug_result_time_decorator
    def compute(self, consecutive_binds=False, with_fast_map=False):
        arguments = self.arguments
        functions = self.functions
        # If functions is a function or a list with only one function
        if isinstance(functions, Callable) or isinstance(functions, list) and len(functions) == 1 and isinstance(functions[0], Callable):
            # Transform functions into a list with the length of the arguments list and the function repeated
            functions = [functions] * len(arguments)

        # If arguments is a list and functions is a list and the length of the arguments list is not equal to the length of the functions list
        if isinstance(arguments, list) and isinstance(functions, list) and len(arguments) != len(functions):
            # Raise an exception because the arguments are invalid
            raise Exception(
                'Arguments and functions must have the same length')

        # If with_fast_map is True
        if with_fast_map:

            # Apply fast_map_async using self.consecutive_bind_caller to the arguments, functions lists and with_fast_map equal to True if consecutive_binds is True
            # Else apply fast_map_async using self.bind_caller to the arguments, functions lists and with_fast_map equal to True if consecutive_binds is False
            t = fast_map_async(self.consecutive_bind_caller, arguments, functions, [{}] * len(arguments), [True] * len(arguments), on_result=(
                self.on_result)) if consecutive_binds else fast_map_async(self.bind_caller, arguments, functions, [{}] * len(arguments), [True] * len(arguments), on_result=(self.on_result))
            # Join the thread
            t.join()
            # Return the results list
            return self.results

        # Processes list
        processes = []
        # Return_dict dictionary
        return_dict = Manager().dict()
        # For each argument in the arguments list
        for i in range(len(arguments)):
            # If consecutive_binds is True target is equal to consecutive_bind_caller else target is equal to bind_caller
            target = self.consecutive_bind_caller if consecutive_binds else self.bind_caller
            # Create a process using target and the arguments, functions lists and return_dict dictionary and False (not with_fast_map)
            p = Process(target=target, args=(
                arguments[i], functions[i], return_dict, False))
            # Start the process
            p.start()
            # Add the process to the processes list
            processes.append(p)

        # For each process in the processes list
        for p in processes:
            # Join the process
            p.join()

        # Return a list with the values of the return_dict dictionary ordered by the arguments list order
        return [str(i[1])[:10] if isinstance(i[1], (int, float)) else i[1] for i in (sorted(return_dict.items(), key=lambda x: arguments.index(list(map(int, x[0].split('$')[0].split())))))]

    # Method that creates a monad, binds it to an argument and a function, updates the return_dict with the result and returns the result
    def bind_caller(self, argument, f, return_dict, with_fast_map=False):
        # Creates a monad and binds it to a function and an argument
        monad = FailureMonad(argument).bind(f)

        # If with_fast_map is True
        if with_fast_map:
            # creates a monad, binds it to a function and an argument and returns the value of the monad
            return monad.value

        # Gets the value of the monad
        result = monad.error_status if monad.value is None else monad.value

        # Updates the return_dict with the result, uses the argument concatenated with the id of the monad as the key
        return_dict[f'{str(argument)}${str(monad.id)}'] = result

        # Returns the result
        return result

    # Method that creates a monad, binds it to arguments and functions, updates the return_dict with the result and returns the result
    def consecutive_bind_caller(self, arguments, functions, return_dict={}, with_fast_map=False):
        # If the arguments are a list creates a monad with the first argument of the list, else creates a monad with the argument
        monad = FailureMonad(arguments[0]) if isinstance(
            arguments, list) else FailureMonad(arguments)
        # If the arguments are not a list or the length of the arguments is 1, consecutive_binds the monad to the functions, else consecutive_binds the monad to the functions and the other arguments
        monad = monad.consecutive_binds(functions) if not isinstance(arguments, list) or len(
            arguments) == 1 else monad.consecutive_binds(functions, arguments[1:])

        # If with_fast_map is True
        if with_fast_map:
            # Returns the value of the monad
            return monad.error_status if monad.value is None else monad.value

        # Gets the value of the monad
        result = monad.error_status if monad.value is None else monad.value

        # Updates the return_dict with the result, concatenates each argument and the id of the monad to use to be used as the key
        string = ''.join(f'{str(argument)} ' for argument in arguments)
        return_dict[f'{string}${str(monad.id)}'] = result
        # Returns the result
        return result


class LazyMonad:

    def __init__(self, value: object):

        if isinstance(value, Callable):
            self.compute = value
        else:
            def return_val():
                return value

            self.compute = return_val

    def bind(self, f: Callable, *args, **kwargs) -> 'FailureMonad':

        def f_compute():
            return f(self.compute(), *args, **kwargs)

        return LazyMonad(f_compute)

    def consecutive_binds(self, f, *args, **kwargs) -> 'LazyMonad':

        if isinstance(f, Callable) or isinstance(f, list) and len(f) == 1 and isinstance(f[0], Callable):
            if isinstance(f, list) and len(f) == 1 and isinstance(f[0], Callable):
                f = f[0]
            if len(args) == 1 and not isinstance(args[0], list):

                return self.bind(f, *args, **kwargs)

            elif len(args) == 1 and isinstance(args[0], list):

                last = self.bind(f, args[0][0], **kwargs)

                for i in range(1, len(args[0])):
                    last = last.bind(f, args[0][i], **kwargs)

                return last

            else:

                last = self.bind(f, args[0], **kwargs)

                for i in range(1, len(args)):
                    last = last.bind(f, args[i], **kwargs)

                return last
        elif isinstance(f, list) and len(args) == 1 and isinstance(args[0], list) and len(f) == len(args[0]):

            last = self.bind(
                f[0], args[0][0], **kwargs)

            for i in range(1, len(args[0])):
                last = last.bind(f[i], args[0][i], **kwargs)

            return last
        else:
            raise Exception('Invalid arguments')

###NOTES###
# Currently everything works for functions that receive 1 or 2 arguments.
# How to make it work for functions that receive more than 2 arguments?
# Not sure if it is possible to do it with the current implementation.
# What are monads usefull for?
