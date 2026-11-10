import sys

def collecting_max_coins(rows, cols, nums):
    dp = [[0]*cols for _ in range(rows)]
    dp[0][0] = nums[0][0]
    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                dp[i][j] = dp[i][j-1] + nums[i][j]
            elif j == 0:
                dp[i][j] = dp[i-1][j] + nums[i][j]
            else:
                dp[i][j] = max((dp[i-1][j] + nums[i][j]), (dp[i][j-1] + nums[i][j]))
    return dp[rows-1][cols-1]

def main():
    rows, cols = map(int, sys.stdin.readline().strip().split())
    nums = []
    for _ in range(rows):
        nums.append(list(map(int, sys.stdin.readline().strip().split())))
    print(collecting_max_coins(rows, cols, nums))

if __name__ == "__main__":
    main()