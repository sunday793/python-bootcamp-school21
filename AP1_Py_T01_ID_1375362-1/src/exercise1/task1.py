import sys

def scalar_product(vec1: list[float], vec2: list[float])->float: 
    result = vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2]
    return result

def main():
    vec1 = list(map(float, sys.stdin.readline().strip().split()))
    vec2 = list(map(float, sys.stdin.readline().strip().split()))
    print(scalar_product(vec1, vec2))
    

if __name__ == "__main__":
    main()