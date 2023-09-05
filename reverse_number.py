# Reverse Integer
# 1- Get the last digit
# 2 - Multypling number by base number move to left
# 3 -disision of number by base (move to right)
# 4 sum of the multiplied number and the last digit

#  get the multiplying number of an integer
# multiply=number*base?
# 3*10=30
# move to left


def reverse_integer(x):
    if x < 0:
        sign = -1
        x *= -1
    else:
        sign = 1

    # Convert the integer to a string, reverse it, and convert it back to an integer
    reversed_str = str(x)[::-1]
    reversed_int = int(reversed_str)

    # Apply the original sign to the reversed integer
    reversed_int *= sign

    return reversed_int

# Example usage:
number = -12345
reversed_number = reverse_integer(number)
print(f"Original number: {number}")
print(f"Reversed number: {reversed_number}")
