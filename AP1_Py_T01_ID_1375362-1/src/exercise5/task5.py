import sys

def char_to_digit(char):
    return ord(char) - ord('0')

def is_digit(char):
    return '0' <= char <= '9'

def convert_string_to_float(string: str):
    if not string:
        return None

    i = 0
    sign = 1

    if string[i] == "+" or string[i] == "-":
        if string[i] == "-":
            sign = -1
        i += 1

    if i >= len(string) or not is_digit(string[i]):
        return None

    int_part = 0

    while i < len(string) and is_digit(string[i]):
        int_part = int_part*10 + char_to_digit(string[i])
        i+=1

    frac_part = 0
    frac_digits = 0

    if i < len(string):
        if string[i] != ".":
            return None
        i+=1
        if i >= len(string) or not is_digit(string[i]):
            return None
        while i < len(string) and is_digit(string[i]):
            frac_part = frac_part * 10 + char_to_digit(string[i])
            frac_digits+=1
            i+=1

    if i != len(string):
        return None

    divisor = 1
    for _ in range(frac_digits):
        divisor *= 10

    numerator = int_part * divisor + frac_part

    return (sign, numerator, divisor)

def format_doubled(sign, numerator, divisor) -> str:
    scaled = sign * numerator * 2000

    if scaled >= 0:
        q = scaled // divisor
        r = scaled % divisor
        if 2 * r  >= divisor:
            q+=1
    else:
        a = -scaled
        q = a//divisor
        r = a%divisor
        if 2 * r >= divisor:
            q += 1
        q = -q

    rounded = q

    negative = (rounded < 0) or (rounded == 0 and sign < 0)

    if rounded < 0:
        rounded = -rounded

    int_part = rounded // 1000
    frac_part = rounded % 1000

    frac_str = str(frac_part)
    while len(frac_str) < 3:
        frac_str = '0' + frac_str

    out = str(int_part) + '.' + frac_str
    if negative:
        out = '-' + out

    return out

def main() -> None:
    
    string = sys.stdin.readline().strip()
    num = convert_string_to_float(string)

    if num is None:
        print("Invalid input format")
        return

    sign, numerator, divisor = num
    print(format_doubled(sign, numerator, divisor))


if __name__ == "__main__":
    main()