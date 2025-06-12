from flask import Flask, request, render_template, jsonify
import webbrowser
from threading import Timer
import json

app = Flask(__name__)

def is_connected(graph):
    if not graph:
        return True
    visited = set()
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
    start = next(iter(graph))
    dfs(start)
    return len(visited) == len(graph)

def is_undirected(graph):
    for v in graph:
        for neighbor in graph[v]:
            if v not in graph.get(neighbor, []):
                return False
    return True

def find_triangles(graph):
    triangles = []
    for v in graph:
        for u in graph[v]:
            if u > v:
                for w in graph[v]:
                    if w > u and w in graph[u]:
                        triangles.append([v, u, w])
    return triangles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_graph():
    try:
        graph = json.loads(request.form['graph'])
        if not is_undirected(graph):
            return jsonify({'error': 'The graph is directed — analysis is only for undirected graphs.'})
        connected = is_connected(graph)
        triangles = find_triangles(graph)
        return jsonify({
            'connected': connected,
            'triangles': triangles
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = 5000
    url = f"http://127.0.0.1:{port}"

    Timer(1, lambda: webbrowser.open(url)).start()

    app.run(port=port)
