import sys

def counting_numbers(nums):
    return len(set(nums))

def main():
    n = int(sys.stdin.readline().strip())
    nums = [int(sys.stdin.readline().strip()) for _ in range(n)]
    print(counting_numbers(nums))

if __name__ == "__main__":
    main()