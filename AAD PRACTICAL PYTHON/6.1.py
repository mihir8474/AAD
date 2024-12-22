from flask import Flask,render_template,request
app=Flask(__name__)
def matrix_chain_order(p):
    n=len(p) - 1
    m=[[0 for _ in range(n)] for _ in range(n)]
    s = [[0 for _ in range(n)] for _ in range(n)]
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                q = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k
    return m, s
def optimal_parenthesization(s, i, j):
    if i == j:
        return f"A{i+1}"
    else:
        return f"({optimal_parenthesization(s, i, s[i][j])} * {optimal_parenthesization(s, s[i][j] + 1, j)})"
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        dims = request.form['dimensions']
        p = list(map(int, dims.split(',')))
        m, s = matrix_chain_order(p)
        min_cost = m[0][-1]
        optimal_solution = optimal_parenthesization(s, 0, len(p) - 2)
        n = len(p) - 1
        m_table = [[None for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                m_table[i][j] = m[i][j] if j >= i else None
        result = {
            'min_cost': min_cost,
            'optimal_solution': optimal_solution,
            'm_table': m_table,
            'dimensions': dims
        }
    return render_template('prac6.html', result=result)
if __name__ == '__main__':
    app.run(debug=True)
