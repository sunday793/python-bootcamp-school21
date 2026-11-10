import sys

def is_palindrome(number: int)->bool:

    if number < 0:
        return False
    
    if number < 10:
        return True

    original = number
    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number //= 10

    return original == reversed_number


def main():
    number = int(sys.stdin.readline().strip())
    print(is_palindrome(number))

if __name__ == "__main__":
    main()