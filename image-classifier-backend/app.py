from flask import Flask, request
import csv

app = Flask(__name__)


def csv_to_dict(csv_file_path):
    data_dict = {}
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            key = row['Image']
            value = row['Results']
            data_dict[key] = value
    return data_dict


file_name_mapping = csv_to_dict('./csv/Results.csv')
print(file_name_mapping)


@app.route('/', methods=['POST'])
def process_image_and_csv():
    image_file = request.files['inputFile']
    image_file_name = image_file.filename
    response_str = f"{image_file_name}:{file_name_mapping[image_file_name.split('.')[0]]}"
    return response_str


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=False)
