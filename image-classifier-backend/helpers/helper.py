import csv
def find_results(image_filename, csv_file_path):
    print(image_filename)
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['Image'] == image_filename:
                return row['Results']
    return None
