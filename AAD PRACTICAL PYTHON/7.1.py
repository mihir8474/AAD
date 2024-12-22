from flask import Flask, request, render_template
app = Flask(__name__)
def fractional_knapsack(values, weights, capacity):
    n = len(values)
    value_weight_ratio = [(values[i]/weights[i], i) for i in range(n)]
    value_weight_ratio.sort(reverse=True, key=lambda x: x[0])
    total_value = 0
    total_weight = 0
    knapsack_contents = []
    for ratio, index in value_weight_ratio:
        if total_weight + weights[index] <= capacity:
            total_value += values[index]
            total_weight += weights[index]
            knapsack_contents.append((index+1, values[index], weights[index], 1))  # 1 means full item taken
        else:
            remaining_weight = capacity - total_weight
            fraction = remaining_weight / weights[index]
            total_value += values[index] * fraction
            total_weight += remaining_weight
            knapsack_contents.append((index+1, values[index], weights[index], fraction))
            break
    return total_value, knapsack_contents
def parse_input(input_str):
    try:
        return [float(x) for x in input_str.strip().split()]
    except ValueError:
        return None  
@app.route('/')
def home():
    return render_template('prac7.1.html')
@app.route('/solve', methods=['POST'])
def solve():
    try:
        n = int(request.form['n'])  
        capacity = float(request.form['capacity'])   
        values_input = request.form['values']
        weights_input = request.form['weights']
        values = parse_input(values_input)
        weights = parse_input(weights_input)
        if values is None or weights is None or len(values) != n or len(weights) != n:
            return "Invalid input. Please enter space-separated numbers."
        max_value, knapsack_contents = fractional_knapsack(values, weights, capacity)
        return render_template('prac7.2.html', max_value=max_value, contents=knapsack_contents)
    except ValueError:
        return "Invalid input. Please check the values and weights."
if __name__ == '__main__':
    app.run(debug=True)
