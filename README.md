
# Functional Programming in Python

An attempt to improve the [Functional programming paradigm supported by Python](https://opensource.com/article/19/10/python-programming-paradigms).


## Monads
Since the start of my Computer Science course, I became quite affictionate to the concept of [functional programming](https://www.geeksforgeeks.org/functional-programming-paradigm/#:~:text=Functional%20programming%20is%20a%20programming,is%20%E2%80%9Chow%20to%20solve%E2%80%9D.), one of the key concepts of the paradigm are [monads](https://en.wikipedia.org/wiki/Monad_(functional_programming)) which I tried to implement in Python.

- Functional languages use monads to turn complicated sequences of functions into succinct pipelines that abstract away control flow, and side-effects.

- Monads provide a way to structure a program.

- They can be used (along with abstract data types) to allow actions (e.g. mutable variables) to be implemented safely.



## The Monads.py file
### 3 monad classes:

- Maybe Monads:
It can bind and flag if it contais a value.

- Failure Monads:
It can bind, consecutively bind and abstract exceptions.

- Lazy Monads:
It can bind, consecutively bind and late compute.

### A parallelazible pool of Failure Monads:

If you want to use many Failure Monads that do not deppend on each other, why not parallelize it?
Using this class you can choose: 
- If your monads will bind consecutively
- If you parallelize the pool using [Multiprocessing](https://docs.python.org/3/library/multiprocessing.html) or [Fast Map](https://pypi.org/project/fast-map/).

## Documentation

#### Import all classes from the Monads.py file

```http
  from Monads import * 
```

#### Create a Maybe Monad with a value inside:

```http
  MaybeMonad(value)
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |

#### Bind a Maybe monad with a function:

```http
  MaybeMonad(value).bind(function)
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |
| `function` | `function` | **Not optional**. A funtion to bind the value of the monad with.  |

#### Get the value from a Maybe monad:

```http
  MaybeMonad(value).bind(function).value
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |
| `function` | `function` | **Not optional**. A funtion to bind the value of the monad with.  |

#### Example:

```http
  def square(x):
    return x**2
  print(MaybeMonad(100).bind(square).value)
```


#### Returns:

```http
  10000 #It applied the function to the value of the monad.
```

#### Example:

```http
  def square(x):
    return x**2
  print(MaybeMonad(100).bind(square).bind(square).value)
```


#### Returns:

```http
  1000000 #It applied the function to the value of the monad twice
```

#### Create a Failure Monad with a value inside:
