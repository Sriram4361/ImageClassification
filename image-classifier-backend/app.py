from flask import Flask, request
from helpers.helper import find_results

app = Flask(__name__)


# @app.route('/')
# def index():
#     return 'Hello, World!'


@app.route('/', methods=['POST'])
def process_image_and_csv():
    # Get the uploaded image file
    print(request.host)
    image_file = request.files['inputFile']
    # print(image_file)
    image_file_name = image_file.filename
    csv_file_path = "./csv/Results.csv"

    results = find_results(image_file_name.split('.')[0], csv_file_path)

    # Generate the response string
    response_str = f"{image_file_name}:{results}"

    # Return the response
    return response_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
