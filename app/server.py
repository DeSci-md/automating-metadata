from flask import Flask, request, jsonify
import langchain_api  # Import your script

app = Flask(__name__)

@app.route('/invoke-script', methods=['POST'])
def invoke_script():
    data = request.json  # Assuming JSON data is sent from the web app
    # Call your script with the appropriate inputs
    output = langchain_api.run(data['node'], data['doi'])
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)