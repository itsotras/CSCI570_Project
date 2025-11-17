import sys
import time, tracemalloc

delta = 30  # gap penalty

alpha = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0},
}

def basic_align(X: str, Y: str):
    """
    Input:  Two strings X, Y (over alphabet {A, C, G, T}).
    Output: (cost, aligned_X, aligned_Y)
        cost       : minimum alignment cost (int)
        aligned_X  : aligned version of X with '_' gaps (str)
        aligned_Y  : aligned version of Y with '_' gaps (str)
    """
    m, n = len(X), len(Y)

    # 1) Create DP table and parent table
    #    dp[i][j] = minimum cost to align X[0..i-1] with Y[0..j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # parent[i][j] stores where dp[i][j] comes from:
    #   0: diagonal (i-1, j-1)  -> X[i-1] aligned with Y[j-1]
    #   1: from up   (i-1, j)   -> X[i-1] aligned with gap
    #   2: from left (i,   j-1) -> gap aligned with Y[j-1]
    parent = [[-1] * (n + 1) for _ in range(m + 1)]

    # 2) Initialize first row / first column
    # dp[i][0]: X[0..i-1] vs empty string Y -> i gaps
    for i in range(1, m + 1):
        dp[i][0] = i * delta
        parent[i][0] = 1  # from up (delete a character from X)

    # dp[0][j]: empty X vs Y[0..j-1] -> j gaps
    for j in range(1, n + 1):
        dp[0][j] = j * delta
        parent[0][j] = 2  # from left (delete a character from Y)

    # 3) Fill the DP table
    for i in range(1, m + 1):
        xi = X[i - 1]
        for j in range(1, n + 1):
            yj = Y[j - 1]

            # Three possible transitions:
            # 1) align xi with yj  (diagonal)
            cost_match = dp[i - 1][j - 1] + alpha[xi][yj]
            # 2) align xi with gap (from up)
            cost_up    = dp[i - 1][j] + delta
            # 3) align gap with yj (from left)
            cost_left  = dp[i][j - 1] + delta

            # Choose the minimum cost and record the direction
            best = cost_match
            par = 0  # diagonal by default
            if cost_up < best:
                best = cost_up
                par = 1
            if cost_left < best:
                best = cost_left
                par = 2

            dp[i][j] = best
            parent[i][j] = par

    # 4) Backtracking: reconstruct the alignment from (m, n) to (0, 0)
    i, j = m, n
    aligned_X = []
    aligned_Y = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and parent[i][j] == 0:
            # from diagonal: X[i-1] aligned with Y[j-1]
            aligned_X.append(X[i - 1])
            aligned_Y.append(Y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or parent[i][j] == 1):
            # from up: X[i-1] aligned with gap
            aligned_X.append(X[i - 1])
            aligned_Y.append('_')
            i -= 1
        else:
            # from left: gap aligned with Y[j-1]
            aligned_X.append('_')
            aligned_Y.append(Y[j - 1])
            j -= 1

    # We built the alignment from the end to the start, so reverse it
    aligned_X = ''.join(reversed(aligned_X))
    aligned_Y = ''.join(reversed(aligned_Y))
    cost = dp[m][n]

    return cost, aligned_X, aligned_Y


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r") as f:
        file_lines = [file_line.strip() for file_line in f if file_line.strip()]
        X = file_lines[0]
        Y = file_lines[1]
        
    tracemalloc.start()
    start = time.time()

    cost, ax, ay = basic_align(X, Y)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time_ms = (end - start) * 1000
    memory_kb = peak / 1024

    with open(output_path, "w") as f:
        f.write(str(cost) + "\n")
        f.write(ax + "\n")
        f.write(ay + "\n")
        f.write(f"{time_ms:.3f}\n Milliseconds")
        f.write(f"{memory_kb:.3f}\n Kilobytes")

