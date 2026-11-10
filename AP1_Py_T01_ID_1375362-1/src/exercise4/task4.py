import sys

def generating_pascal_triangle(number: int) -> None:
    triangle = []

    for i in range(number):
        row = [1] * (i+1)
        for j in range(1,i):
            row[j] = triangle[i-1][j-1] + triangle[i-1][j]
        triangle.append(row)
        print(" ".join(map(str, row)))

def main() -> None:
    try:
        number = int(sys.stdin.readline().strip())
        if number <= 0:
            print("Natural number was expected")
            return
        generating_pascal_triangle(number)
        
    except ValueError:
        print("Natural number was expected")

if __name__ == "__main__":
    main()