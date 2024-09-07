from flask import Flask, Response, json, request, jsonify
import pandas as pd
import numpy as np
from tasks import MissingValuesTask, DuplicateRowsTask

app = Flask(__name__)

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline_api():
    try:
        data = request.json

        file_path = data.get('file_path', 'dataset.csv')
        task_order = data.get('task_order', [])
        task_params = data.get('task_params', {})

        # Load dataset
        df = pd.read_csv(file_path)

        # Print the columns of the loaded dataset
        print("Dataset columns:", df.columns.tolist())

        # Define tasks with parameters from API request
        tasks = {
            'missing_values': MissingValuesTask(
                columns=task_params.get('missing_values', {}).get('columns', []),
                thresholds=task_params.get('missing_values', {}).get('thresholds', {})
            ),
            'duplicate_rows': DuplicateRowsTask(
                subset=task_params.get('duplicate_rows', {}).get('subset', [])
            ),
        }

        # Execute tasks in the order specified
        results = {}
        for task_name in task_order:
            if task_name in tasks:
                task = tasks[task_name]
                result = task.execute(df)
                
                # Convert NumPy types to native Python types
                if isinstance(result, dict):
                    for key, value in result.items():
                        if isinstance(value, dict):
                            result[key] = {sub_k: float(sub_v) if isinstance(sub_v, (float, np.float64)) 
                                           else int(sub_v) if isinstance(sub_v, (int, np.int64)) 
                                           else bool(sub_v) if isinstance(sub_v, (np.bool_,)) 
                                           else sub_v 
                                           for sub_k, sub_v in value.items()}
                        elif isinstance(value, (int, np.int64)):
                            result[key] = int(value)
                        elif isinstance(value, (float, np.float64)):
                            result[key] = float(value)
                        elif isinstance(value, (np.bool_,)):
                            result[key] = bool(value)
                
                results[task_name] = result
            else:
                results[task_name] = "Task not found"

        # Reorder results to match task_order
        json_response = json.dumps({"status": "success", "results": results}, sort_keys=False)
        return Response(json_response, mimetype='application/json')
    
    except Exception as e:

        error_response = json.dumps({"status": "error", "message": str(e)})
        return Response(error_response, mimetype='application/json', status=500)

if __name__ == '__main__':
    app.run(debug=True)
