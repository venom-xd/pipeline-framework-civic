Configurable Data Processing Pipeline

This project implements a configurable data processing pipeline using Flask. The pipeline allows you to identify missing values and duplicate rows in a dataset. It is configurable through API requests, making it highly flexible and reusable.


Features

Missing Values Task: Identifies the percentage of missing values in specified columns and checks if it exceeds the given threshold.
Duplicate Rows Task: Identifies duplicate rows based on specified columns.
Task Serialization: Tasks are executed in the order specified in the request, and results are serialized into a structured JSON format.



Requirements
To run this project, you'll need:

Python 3.8 or higher
Flask
Pandas
NumPy
Installation

Clone the repository:

git clone https://github.com/venom-xd/pipeline-framework-civic.git

cd pipeline-framework-civic

Install the dependencies:

pip install -r requirements.txt

Running the Application

Place your dataset in the project directory and name it dataset.csv. You can specify another dataset name in the API request if needed.

Run the Flask application:

python app.py
The API will be available at http://127.0.0.1:5000/run_pipeline.

API Usage
Send POST requests to http://127.0.0.1:5000/run_pipeline to execute the data processing tasks. You can specify multiple tasks in the request, and they will be executed in the order provided.

Request Format
The API request should contain:

file_path: Path to the CSV file.
task_order: List of tasks to execute in the order they should be run.
task_params: Parameters for each task.


Example 1: Identifying Missing Values
Request: curl -X POST http://127.0.0.1:5000/run_pipeline
-H "Content-Type: application/json"
-d "{"file_path": "dataset.csv", "task_order": ["missing_values"], "task_params": {"missing_values": {"columns": ["Name", "Age", "Email"], "thresholds": {"Name": 0, "Age": 0, "Email": 0}}}}"

Response: {"status": "success", "results": {"missing_values": {"Name": {"missing_percentage": 2.94, "exceeds_threshold": true}, "Age": {"missing_percentage": 1.96, "exceeds_threshold": true}, "Email": {"missing_percentage": 3.92, "exceeds_threshold": true}}}}



Example 2: Identifying Duplicate Rows
Request: curl -X POST http://127.0.0.1:5000/run_pipeline
-H "Content-Type: application/json"
-d "{"file_path": "dataset.csv", "task_order": ["duplicate_rows"], "task_params": {"duplicate_rows": {"subset": ["ID", "Name", "Age", "Email"]}}}"

Response: {"status": "success", "results": {"duplicate_rows": {"duplicate_count": 2, "columns_checked": ["ID", "Name", "Age", "Email"]}}}



Example 3: Running Multiple Tasks (Missing Values, then Duplicates)
Request: curl -X POST http://127.0.0.1:5000/run_pipeline
-H "Content-Type: application/json"
-d "{"file_path": "dataset.csv", "task_order": ["missing_values", "duplicate_rows"], "task_params": {"missing_values": {"columns": ["Name", "Age", "Email"], "thresholds": {"Name": 0, "Age": 0, "Email": 0}}, "duplicate_rows": {"subset": ["ID", "Name", "Age", "Email"]}}}"

Response: {"status": "success", "results": {"missing_values": {"Name": {"missing_percentage": 2.94, "exceeds_threshold": true}, "Age": {"missing_percentage": 1.96, "exceeds_threshold": true}, "Email": {"missing_percentage": 3.92, "exceeds_threshold": true}}, "duplicate_rows": {"duplicate_count": 2, "columns_checked": ["ID", "Name", "Age", "Email"]}}}



Example 4: Running Multiple Tasks (Duplicates first, then Missing Values)
Request: curl -X POST http://127.0.0.1:5000/run_pipeline
-H "Content-Type: application/json"
-d "{"file_path": "dataset.csv", "task_order": ["duplicate_rows", "missing_values"], "task_params": {"duplicate_rows": {"subset": ["ID", "Name", "Age", "Email"]}, "missing_values": {"columns": ["Name", "Age", "Email"], "thresholds": {"Name": 0, "Age": 0, "Email": 0}}}}"

Response: {"status": "success", "results": {"duplicate_rows": {"duplicate_count": 2, "columns_checked": ["ID", "Name", "Age", "Email"]}, "missing_values": {"Name": {"missing_percentage": 2.94, "exceeds_threshold": true}, "Age": {"missing_percentage": 1.96, "exceeds_threshold": true}, "Email": {"missing_percentage": 3.92, "exceeds_threshold": true}}}}



Serialization and Execution of Tasks

Tasks are executed in the order specified in the task_order list. The pipeline ensures that each task is run sequentially, and the results are serialized into a JSON response after the completion of all tasks.

For example, if ["missing_values", "duplicate_rows"] is the task order, the missing values task will be executed first, followed by the duplicate rows task. Similarly, if ["duplicate_rows", "missing_values"] is the order, the duplicate rows task will run first.

Serialized Output
The serialized output of the pipeline is returned in a structured JSON format, where each task's result is included under the respective task's name. Here is an example of a serialized output:

{ "status": "success", "results": { "missing_values": { "Name": {"missing_percentage": 2.94, "exceeds_threshold": true}, "Age": {"missing_percentage": 1.96, "exceeds_threshold": true}, "Email": {"missing_percentage": 3.92, "exceeds_threshold": true} }, "duplicate_rows": { "duplicate_count": 2, "columns_checked": ["ID", "Name", "Age", "Email"] } } }

This output format makes it easy to understand the results of each task, and the structure allows for further extension by adding more tasks.

