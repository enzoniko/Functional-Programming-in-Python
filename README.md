
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

```http
  FailureMonad(value)
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |

#### Bind a Failure Monad with a function:

```http
  FailureMonad(value).bind(function)
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |
| `function` | `function` | **Not optional**. A funtion to bind the value of the monad with.  |

#### Get the value from a Failure Monad:

```http
  FailureMonad(value).bind(function).value
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |
| `function` | `function` | **Not optional**. A funtion to bind the value of the monad with.  |

#### Example:

```http
  def square(x):
    return x**2
  print(FailureMonad(100).bind(square).value)
```

#### Returns:

```http
  10000 #It applied the function to the value of the monad.
```

#### Example:

```http
  def square(x):
    return x**2
  print(FailureMonad(100).bind(square).bind(square).value)
```


#### Returns:

```http
  1000000 #It applied the function to the value of the monad twice
```

#### Multiple argument functions support:

```http
  def div(x, y):
    return x/y
  print(FailureMonad(100).bind(div, 10).value)
```


#### Returns:

```http
  10 #It applied the function to the value of the monad and the argument.
```

#### Example:

```http
  def div(x, y):
    return x/y
  print(FailureMonad(100).bind(div, 10).bind(div, 10).value)
```


#### Returns:

```http
  1 #It applied the function to the value of the monad and the argument twice.
```

#### The key difference of Failure Monads is error handling:

```http
  def div(x, y):
    return x/y
  print(FailureMonad(100).bind(div, 0).value)
```


#### Returns:

```http
  None #Instead of rising an Exception it returs None and updates the error status.
```

#### Get the error status of a failure monad
```http
  
  FailureMonad(value).bind(function).error_status
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |
| `function` | `function` | **Not optional**. A funtion to bind the value of the monad with.  |

#### Example:

```http
  def div(x, y):
    return x/y
  print(FailureMonad(100).bind(div, 0).error_status)
  #It returns a dictionary containing every info of the exception/error.
```


#### Create a Lazy Monad with a value inside:

```http
  LazyMonad(value)
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |

#### Bind a Lazy Monad with a function:

```http
  LazyMonad(value).bind(function)
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |
| `function` | `function` | **Not optional**. A funtion to bind the value of the monad with.  |

#### The key difference of Lazy monads is late computing, it only computes when asked.

```http
  FailureMonad(value).bind(function).compute()
```

| Parameter  | Type      | Description                           |
| :---------- | :--------- | :---------------------------------- |
| `value` | `number` | **Not optional**. The value of your monad.  |
| `function` | `function` | **Not optional**. A funtion to bind the value of the monad with.  |

#### Example:

```http
  def square(x):
    return x**2
  print(LazyMonad(100).bind(square).compute())
```

#### Returns:

```http
  10000 #It applied the function to the value of the monad.
```

#### Example:

```http
  def square(x):
    return x**2
  print(LazyMonad(100).bind(square).bind(square).compute())
```


#### Returns:

```http
  1000000 #It applied the function to the value of the monad twice
```

#### Multiple argument functions support:

```http
  def div(x, y):
    return x/y
  print(LazyMonad(100).bind(div, 10).compute())
```


#### Returns:

```http
  10 #It applied the function to the value of the monad and the argument.
```

#### Example:

```http
  def div(x, y):
    return x/y
  print(LazyMonad(100).bind(div, 10).bind(div, 10).compute())
```


#### Returns:

```http
  1 #It applied the function to the value of the monad and the argument twice.
```

#### Since Lazy Monads do not handle errors like Failure Monads:

```http
  def div(x, y):
    return x/y
  print(LazyMonad(100).bind(div, 0))
  # This does not rise an exception because it hasn't computed it yet
```

#### So if we compute it, then it rises an Exception because we are dividing by zero:

```http
  def div(x, y):
    return x/y
  print(LazyMonad(100).bind(div, 0).compute())
  # Rises an Exception because we can't divide by zero.
```

#### Consecutive Binds Method:
