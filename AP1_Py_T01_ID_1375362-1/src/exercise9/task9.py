import sys

def derivative(n, x, coeffs):
    result = 0.0
    for i, a in enumerate(coeffs):
        degree = n-i
        if degree == 0:
            continue
        result += degree * a * (x ** (degree - 1))
    return result


def main():
    first = sys.stdin.readline().split()
    n = int(first[0])
    x = float(first[1])
    coeffs = [float(sys.stdin.readline()) for _ in range(n + 1)]
    result = derivative(n, x, coeffs)
    print(f"{result:.3f}")

if __name__ == "__main__":
    main()