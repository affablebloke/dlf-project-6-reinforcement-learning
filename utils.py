import csv


def write_csv_header(labels, file_output):
    with open(file_output, 'w') as csvfile:
        labels = [label for label in labels]
        writer = csv.writer(csvfile)
        writer.writerow(labels)


def write_stats_to_row(rows, file_output):
    with open(file_output, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)
