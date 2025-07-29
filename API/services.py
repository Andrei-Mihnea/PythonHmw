def power(a,b):
    """Calculate a raised to the power of b."""
    return a ** b

def fibonacci(n):
    """Return a list of Fibonacci numbers up to index n (inclusive), starting from 1, 1."""
    if n < 0:
        raise ValueError("Fibonacci number is not defined for non-positive indices")
    sequence = [0]
    if n == 0:
        return sequence
    
    sequence.append(1)  

    if n == 1:
        return sequence

    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

    
def factorial(n):
    """Calculate the factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result