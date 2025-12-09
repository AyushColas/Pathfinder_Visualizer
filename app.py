from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from src.algorithms import Graph, dijkstra, astar, PathResult
import time

app = Flask(__name__)
CORS(app)

app.config['JSON_SORT_KEYS'] = False


def result_to_dict(result: PathResult) -> dict:
    return {
        "path": result.path,
        "distance": result.distance,
        "nodes_explored": result.nodes_explored,
        "execution_time_ms": result.execution_time_ms,
        "algorithm": result.algorithm
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Pathfinding API",
        "version": "1.0.0"
    })


@app.route('/api/pathfind/dijkstra', methods=['POST'])
def find_path_dijkstra():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        required_fields = ['graph', 'start', 'end']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        graph = Graph.from_dict(data['graph'])
        start = data['start']
        end = data['end']
        
        result = dijkstra(graph, start, end)
        
        if result is None:
            return jsonify({
                "error": "No path found",
                "start": start,
                "end": end
            }), 404
        
        return jsonify({
            "success": True,
            "result": result_to_dict(result)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/pathfind/astar', methods=['POST'])
def find_path_astar():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        required_fields = ['graph', 'start', 'end']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        graph = Graph.from_dict(data['graph'])
        start = data['start']
        end = data['end']
        heuristic = data.get('heuristic', 'euclidean')
        
        if heuristic not in ['euclidean', 'manhattan']:
            return jsonify({"error": "Invalid heuristic. Use 'euclidean' or 'manhattan'"}), 400
        
        result = astar(graph, start, end, heuristic)
        
        if result is None:
            return jsonify({
                "error": "No path found",
                "start": start,
                "end": end
            }), 404
        
        return jsonify({
            "success": True,
            "result": result_to_dict(result)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/pathfind/compare', methods=['POST'])
def compare_algorithms():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        required_fields = ['graph', 'start', 'end']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        graph = Graph.from_dict(data['graph'])
        start = data['start']
        end = data['end']
        
        results = {}
        
        dijkstra_result = dijkstra(graph, start, end)
        if dijkstra_result:
            results['dijkstra'] = result_to_dict(dijkstra_result)
        
        astar_euclidean = astar(graph, start, end, 'euclidean')
        if astar_euclidean:
            results['astar_euclidean'] = result_to_dict(astar_euclidean)
        
        astar_manhattan = astar(graph, start, end, 'manhattan')
        if astar_manhattan:
            results['astar_manhattan'] = result_to_dict(astar_manhattan)
        
        if not results:
            return jsonify({
                "error": "No path found by any algorithm",
                "start": start,
                "end": end
            }), 404
        
        return jsonify({
            "success": True,
            "start": start,
            "end": end,
            "comparisons": results
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/docs', methods=['GET'])
def api_docs():
    return jsonify({
        "name": "High-Performance Pathfinding API",
        "version": "1.0.0",
        "description": "REST API for graph pathfinding using Dijkstra's and A* algorithms",
        "endpoints": [
            {
                "path": "/api/health",
                "method": "GET",
                "description": "Health check endpoint"
            },
            {
                "path": "/api/pathfind/dijkstra",
                "method": "POST",
                "description": "Find shortest path using Dijkstra's algorithm",
                "body": {
                    "graph": {
                        "nodes": [{"id": "A", "x": 0, "y": 0}],
                        "edges": [{"from": "A", "to": "B", "weight": 1.0}]
                    },
                    "start": "A",
                    "end": "B"
                }
            },
            {
                "path": "/api/pathfind/astar",
                "method": "POST",
                "description": "Find shortest path using A* algorithm",
                "body": {
                    "graph": {},
                    "start": "A",
                    "end": "B",
                    "heuristic": "euclidean|manhattan"
                }
            },
            {
                "path": "/api/pathfind/compare",
                "method": "POST",
                "description": "Compare all algorithms on the same graph"
            }
        ],
        "complexity": {
            "dijkstra": "O((V + E) log V) with binary heap",
            "astar": "O((V + E) log V) with heuristic optimization"
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
