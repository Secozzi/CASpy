[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

# CASPy
_A program that provides a GUI and a CLI to a symbolic computation and computer algebra system python library, SymPy._

<p align="center">
  <img src="https://i.imgur.com/F7wfzQt.png" alt="CASPY logo">
</p>

## CASpy

A Computer Algebra System built using mainly PyQt5 and Sympy

## Installing

Install with `pip` .

```
pip install caspy3
```

## Usage

To start the GUI

```
caspy start
```

### Requirements
Make sure you install all dependencies inside `requirements.txt`.

### Command-line tool

Notes:
Put any negative numbers inside parentheses so the command line tool doesn't think it's an argument. Example: `caspy eval (-1)**2`

```
Usage: caspy [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  deriv  Calculate the derivative.
  eq     Solve an equation.
  eval   Evaluates an expression.
  exp    Expandes an expression.
  integ  Calculate the integral.
  limit  Calculate the limit of an expression.
  pf     Retreives the prime factors of an positive integer.
  simp   Simplifies an expression.
  start  Start the GUI
  web    Choose a number from a list of usable maths websites.
```

#### Flags
`-p, --preview`, Preview instead of calculating <br>
`-o, --output-type`, Select output type, 1 for pretty; 2 for latex and 3 for normal <br>
`-u, --use-unicode`, Use unicode for symbols <br>
`-l, --line-wrap`, Use line wrap on answer <br>

#### Arguments
`-s, --use-scientific`, Notate approximate answer with scientific notation, argument is accuracy <br>
`-a --accuracy`, Accuracy of evaluation <br>

#### deriv
```
Calculate the derivative.

  Usage:
    deriv *expression *variable order at_point
    * = required
  Example:
    > caspy deriv sin(1/ok) ok 3 pi
```

#### eq
```
Solve an equation.

  Usage:
    eq *left_expression *right_expression *variable_to_solve_for solve_type
    * = required
    Use '--solve-type' or '-st' flag to solve equation with SymPy solve, set flag for solveset
  Examples:
    > caspy eq x**x 2 x
    > caspy eq sin(x) 1 x -st
```

#### eval
```
Evaluates an expression.

  Usage:
    eval *expression
    * = required
  Example:
    > caspy eval exp(pi)+3/sin(6)
```


#### exp
```
  Expandes an expression.

  Usage:
    exp *expression
    * = required
  Example:
    > exp (a+b-c)**3
```

#### integ
```
Calculate the integral.

  Usage:
    integ *expression *variable lower_bound upper_bound
    * = required
  Example:
    > caspy integ 1/sqrt(1-x**2) x (-1) 1
```

#### limit
```
Calculate the limit of an expression.

  Usage:
    limit *expression *variable *as_variable_is_approaching side
    * = required
    Both sides as default, + for right side and - for left side
  Example:
    > caspy limit u!**(1/u) u 0 -
```

#### pf
```
Retreives the prime factors of an positive integer.

  Usage:
    pf *number
    * = required
  Example:
    > caspy pf 372

  Note: exact_ans stores factors as dict: '{2: 2, 3: 1, 31: 1}' while approx_ans stores factors as string: '(2**2)*(3**1)*(31**1)'
```

#### simp
```
Simplifies an expression.

  Usage:
    simp *expression
    * = required
  Example:
    > caspy simp sin(x)**2+cos(x)**2
```

#### start
```
Start the GUI
```

#### web
```
Choose a number from a list of usable maths websites. type '-l' for a list of websites and enter a number. The website will be opened in the default browser.

  Usage:
    web number
  Example:
    > caspy web 4
    > caspy web -l
```
