[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

# CASPy
_A program that provides both a GUI and a CLI to SymPy, a symbolic computation and computer algebra system Python library._

<p align="center">
  <img src="https://i.imgur.com/F7wfzQt.png" alt="CASPY logo">
</p>

## Installing

Install with `pip`.

```
pip install caspy3
```

## Usage

To start the GUI

```
caspy start
```

### Command-line tool

```
Usage: caspy [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  deriv    Derive a function.
  diff-eq  Solves a differential equation equation.
  eq       Solves a normal equation.
  eval     Evaluates an expression.
  exp      Expandes an expression.
  integ    Calculate definite and indefinite integrals of expressions.
  limit    Calculate the limit of an expression.
  pf       Retreives the prime factors of an positive integer.
  simp     Simplifies an expression.
  start    Start the GUI.
  sum      Calculate the summation of an expression.
  sys-eq   Solves a system of either normal or differential equations.
  web      Choose a number from a list of usable maths websites and open it...
```

#### Flags
`-p, --preview`, Previews instead of calculating <br>
`-o, --output-type`, Select output type, 1 for pretty; 2 for latex and 3 for normal <br>
`-u, --use-unicode`, Use unicode for symbols <br>
`-l, --line-wrap`, Use line wrap on answer <br>

#### Arguments
`-s, --use-scientific`, Notate approximate answer with scientific notation, argument is accuracy <br>
`-a --accuracy`, Accuracy of evaluation <br>
`-c --copy`, Copies the answer. 1 for exact_ans and 2 for approx_ans and 3 for a list of [exact_ans, approx_ans] <br>

#### Equation specific arguments
`-d --domain`, Give domain to solve for <br>
`-v --verify-domain`, Filter out any solutions that isn't in domain. Doesn't work with solveset. This flag must be set in order for domain to work if it solves with solve and not solveset. Needed for system of equations <br> 

#### deriv
```
Derive a function

    Usage: caspy deriv EXPRESSION VARIABLE [ORDER] [AT_POINT] [FLAGS]

    Example(s):
    >>> caspy deriv x**x x
    >>> caspy deriv sin(1/x) x 3 pi
```

#### diff-eq
```
Solves a differential equation equation.

    Separate equation by either a space or a =, but not both.

    Usage: diff-eq LEFT_EXPRESSION RIGHT_EXPRESSION FUNCTION_TO_SOLVE_FOR [HINT] [FLAGS]

    Example(s):
    >>> caspy diff-eq f'(x) 1/f(x) f(x)
    >>> caspy diff-eq f''(x)+3*f'(x)=x**2 f(x)
```

#### eq
```
Solves a normal equation.

    Separate equation by either a space or a =, but not both.

    Usage: eq LEFT_EXPRESSION RIGHT_EXPRESSION VARIABLE_TO_SOLVE_FOR [SOLVE_TYPE] [FLAGS]

    Example(s):
    >>> caspy eq x**x 2 x
    >>> caspy eq sin(x)=1 x -st
```

#### eval
```
Evaluates an expression.

    After expression you can also subtitute your variables with a value.
    To substitute, simply type the variable to substitute followed by the value separated by a space.

    For example:
    >>> 3**(x+y) x 3 y 5
    => 3**((3)+(5))
    => 6561

    Usage: eval EXPRESSION [VARS_SUB ... ] [FLAGS]

    Example(s):
    >>> caspy eval exp(pi)+3/sin(6)
    >>> caspy eval 3**x x 3
```

#### exp
```
Expandes an expression.

    Usage: exp EXPRESSION [FLAGS]

    Example(s):
    >>> caspy exp (a+b-c)**3
```

#### integ
```
Calculate definite and indefinite integrals of expressions.

    Usage: caspy integ EXPRESSION VARIABLE {LOWER_BOUND UPPER_BOUND} [APPROXIMATE] [FLAGS]

    Example(s):
    >>> caspy integ 1/sqrt(1-x**2) x -1 1
    >>> caspy integ x**x x -1 1 -A
```

#### limit
```
Calculate the limit of an expression.

    Usage: caspy limit EXPRESSION VARIABLE AS_VARIABLE_IS_APPROACHING [SIDE] [FLAGS]

    Example(s):
    >>> caspy limit (1+1/(a*n))**(b*n) n oo
    >>> caspy limit n!**(1/n) n 0 -
```

#### pf
```
Retreives the prime factors of an positive integer.

    Note: exact_ans stores factors as dict: '{2: 2, 3: 1, 31: 1}'
    while approx_ans stores factors as string: '(2**2)*(3**1)*(31**1)'

    Usage: pf NUMBER

    Example(s):
    >>> caspy pf 372
```

#### simp
```
Simplifies an expression.

    Usage: simp EXPRESSION [FLAGS]

    Example(s):
    >>> caspy simp sin(x)**2+cos(x)**2
```

#### start
```
Start the GUI. No options/flags etc
```

#### sum
```
Calculate the summation of an expression.

    Usage: caspy sum EXPRESSION VARIABLE START END [FLAGS]

    \b
    Example(s):
    >>> caspy sum x**k/factorial(k) k 0 oo
    >>> caspy sum k**2 k 1 m
```

#### sys-eq
```
Solves a system of either normal or differential equations.

    Takes number of equations as argument, then will prompt user for all equations

    Usage: sys-eq NO_OF_EQUATIONS [SOLVE_TYPE] [FLAGS]

    Example(s):
    >>> caspy sys-eq 5
    >>> caspy sys-eq 3 -d Integers

```

#### web
```
Choose a number from a list of usable maths websites and open it in default web browser.

    type '-l' for a list of websites and enter a number. The website will be opened in the default browser.

    Usage: web {NUMBER | LIST}

    Example(s):
    >>> caspy web 4
    >>> caspy web -l
```
