import sys
import time, tracemalloc

delta = 30

alpha = {
    'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
    'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
    'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
    'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0},
}


# Compute only the last DP row of aligning X with Y
# Used by the divide & conquer step
def compute_last_row(X, Y):
    # Return the DP costs for aligning the full prefix X[:m] with every
    # prefix of Y (i.e. a list of length n+1 where index j is cost(X, Y[:j])).
    m, n = len(X), len(Y)

    # prev represents dp[0][j] for j=0..n (aligning empty X with prefixes of Y)
    prev = [j * delta for j in range(n + 1)]

    for i in range(1, m + 1):
        xi = X[i - 1]
        # dp[i][0] = i * delta (aligning X[:i] with empty Y)
        curr = [i * delta]

        for j in range(1, n + 1):
            yj = Y[j - 1]

            cost_match = prev[j - 1] + alpha[xi][yj]
            cost_up    = prev[j] + delta
            cost_left  = curr[j - 1] + delta

            curr.append(min(cost_match, cost_up, cost_left))

        prev = curr

    return prev


# Solve small subproblem with regular DP 
def solve_small(X, Y):
    m, n = len(X), len(Y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    parent = [[-1] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = i * delta
        parent[i][0] = 1

    for j in range(1, n + 1):
        dp[0][j] = j * delta
        parent[0][j] = 2

    for i in range(1, m + 1):
        xi = X[i - 1]
        for j in range(1, n + 1):
            yj = Y[j - 1]

            cost_match = dp[i - 1][j - 1] + alpha[xi][yj]
            cost_up    = dp[i - 1][j] + delta
            cost_left  = dp[i][j - 1] + delta

            best = cost_match
            par = 0

            if cost_up < best:
                best = cost_up
                par = 1
            if cost_left < best:
                best = cost_left
                par = 2

            dp[i][j] = best
            parent[i][j] = par

    # Backtrack
    aligned_X = []
    aligned_Y = []

    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and parent[i][j] == 0:
            aligned_X.append(X[i - 1])
            aligned_Y.append(Y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or parent[i][j] == 1):
            aligned_X.append(X[i - 1])
            aligned_Y.append('_')
            i -= 1
        else:
            aligned_X.append('_')
            aligned_Y.append(Y[j - 1])
            j -= 1

    aligned_X.reverse()
    aligned_Y.reverse()

    return ''.join(aligned_X), ''.join(aligned_Y), dp[m][n]



# Main divide & conquer memory-efficient alignment

def align_memory_efficient(X, Y):

    m, n = len(X), len(Y)

    # Base cases
    if m == 0:
        return "_" * n, Y, n * delta

    if n == 0:
        return X, "_" * m, m * delta

    if m == 1 or n == 1:
        return solve_small(X, Y)

    mid = m // 2

    # Compute prefix and suffix costs
    left_cost = compute_last_row(X[:mid], Y)
    right_cost = compute_last_row(X[mid:][::-1], Y[::-1])

    # Find split point
    best_split = 0
    best_val = float("inf")

    for j in range(n + 1):
        val = left_cost[j] + right_cost[n - j]
        if val < best_val:
            best_val = val
            best_split = j

    # Recursively solve halves
    left_X, left_Y, _ = align_memory_efficient(X[:mid], Y[:best_split])
    right_X, right_Y, _ = align_memory_efficient(X[mid:], Y[best_split:])

    return left_X + right_X, left_Y + right_Y, best_val



if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r") as f:
        file_lines = [line.strip() for line in f if line.strip()]
        X = file_lines[0]
        Y = file_lines[1]

    tracemalloc.start()
    start = time.time()

    aligned_X, aligned_Y, cost = align_memory_efficient(X, Y)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time_ms = (end - start) * 1000
    memory_kb = peak / 1024

    with open(output_path, "w") as f:
        f.write(str(cost) + "\n")
        f.write(aligned_X + "\n")
        f.write(aligned_Y + "\n")
        f.write(f"{time_ms:.5f} Milliseconds\n")
        f.write(f"{memory_kb:.5f} Kilobytes\n")