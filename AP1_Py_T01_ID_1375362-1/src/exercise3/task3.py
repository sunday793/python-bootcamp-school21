def read_matrix(file_name: str) -> list[list[int]]:
    matrix = []
    
    with open(file_name, "r") as file:
        for line in file:
            if line.strip():
                row = list(map(int, line.strip().split()))
                matrix.append(row)
    return matrix

def dfs(matrix:list[list[int]], visited:list[list[bool]], i:int, j:int, n:int) -> list[tuple[int,int]]:
    stack = [(i, j)]
    visited[i][j] = True
    component = []

    while stack:
        x, y = stack.pop()
        component.append((x,y))

        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and matrix[nx][ny] == 1:
                visited[nx][ny] = True
                stack.append((nx, ny))

    return component

def is_square(component:list[tuple[int,int]], n:int) -> bool:
    if not component:
        return False

    min_x = min(p[0] for p in component)
    max_x = max(p[0] for p in component)
    min_y = min(p[1] for p in component)
    max_y = max(p[1] for p in component)

    bbox_area = (max_x - min_x + 1) * (max_y - min_y + 1)
    actual_area = len(component)
    fill_ratio = actual_area/bbox_area

    return fill_ratio > 0.85

def count_figures(matrix:list[list[int]]) -> tuple[int,int]:
    n = len(matrix)
    visited = [[False] * n for _ in range(n)]

    squares = 0
    circles = 0

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1 and not visited[i][j]:
                component = dfs(matrix, visited, i, j, n)

                if len(component) > 1:
                    if is_square(component, n):
                        squares += 1
                    else:
                        circles += 1

    return squares, circles


def main() -> None:
    matrix = read_matrix("input.txt")
    squares, circles = count_figures(matrix)
    print(f"{squares} {circles}")
    

if __name__ == "__main__":
    main()