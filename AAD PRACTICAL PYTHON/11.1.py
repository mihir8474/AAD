from flask import Flask, render_template, request
import heapq
app = Flask(__name__)
graph = {
    'A': {'A': 0, 'B': 20, 'C': 30, 'D': float('inf'), 'E': float('inf')},
    'B': {'A': float('inf'), 'B': 0, 'C': float('inf'), 'D': 15, 'E': float('inf')},
    'C': {'A': float('inf'), 'B': float('inf'), 'C': 0, 'D': float('inf'), 'E': 25},
    'D': {'A': float('inf'), 'B': float('inf'), 'C': float('inf'), 'D': 0, 'E': 10},
    'E': {'A': float('inf'), 'B': float('inf'), 'C': float('inf'), 'D': float('inf'), 'E': 0},
}
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

@app.template_filter('format_inf')
def format_inf(value):
    return '∞' if value == float('inf') else value

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    start_node = None
    error_message = None

    if request.method == 'POST':
        start_node = request.form['start_node'].upper()
        if start_node in graph:
            result = dijkstra(graph, start_node)
        else:
            error_message = "Invalid start node. Please enter a valid city (A-E)."

    return render_template('prac11.html', result=result, start_node=start_node, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
