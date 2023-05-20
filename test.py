import sys


def is_electricity_passing(l, n, operations):
    # 金属板の初期化
    board = [[0] * (l + 1) for _ in range(l + 1)]

    for i in range(n):
        a, b, c, d = operations[i]

    # 切断範囲のセルを1に設定
    for x in range(a, c + 1):
        for y in range(b, d + 1):
            board[x][y] = 1

    # (0,0)から(h,h)までの経路を探索するDFS
    def dfs(x, y):
        if x == l and y == l:
            return True

    if x + 1 <= l and board[x + 1][y] == 0:
        if dfs(x + 1, y):
            return True

    if y + 1 <= l and board[x][y + 1] == 0:
        if dfs(x, y + 1):
            return True
        return False

    # (0,0)から(h,h)への経路を探索
    if dfs(0, 0):
        return "YES"
    else:
        # 電気が通らない場合、何回目の操作で通電しなくなったかを計算
        for i in range(n - 1, -1, -1):
            a, b, c, d = operations[i]
        # 操作を無効化
        for x in range(a, c + 1):
            for y in range(b, d + 1):
                board[x][y] = 0

        if not dfs(0, 0):
            return f"{i + 1}NO"

        return "YES"


if __name__ == '__main__':
    l = 10  # 金属板の一辺の長さ
    n = 3  # 操作の回数
    # 各操作を示す座標のリスト

    operations = [(1, 2, 3, 4), (5, 6, 7, 8), (3, 4, 6, 7)]
    result = is_electricity_passing(l, n, operations)
    print(result)
