from flask import Flask, request
import csv
from Utils.SQSInterface import sendReqtoSQS, sendtoS3, receiveResfromSQS

app = Flask(__name__)

# rqSet = set()


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


@app.route('/', methods=['POST'])
def process_image_and_csv():
    image_file = request.files['inputFile']
    image_file_name = image_file.filename
    sendtoS3(image_file_name, image_file)
    sendReqtoSQS(image_file_name)
    return f"{image_file_name}:{receiveResfromSQS(image_file_name)}"
    # return f"{image_file_name}:{image_file_name}"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    app.run(debug=False)
