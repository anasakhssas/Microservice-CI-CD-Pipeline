from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status='healthy'), 200

@app.route('/data', methods=['POST'])
def process_data():
    data = request.json
    # Process the data here
    return jsonify(result='Data processed successfully', input=data), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)