from sys import argv
import csv
import json
import numpy as np


def main():
    filename = argv[1]
    mode = argv[2]
    with open(filename) as csv_file:
        cvs_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0;
        data = {}
        for row in cvs_reader:
            student = {}
            for k, v in row.items():
                if k != 'student':
                    if mode == 'deadlines':
                        student[k] = float(v)
                    else:
                        (date, ex) = (tuple(k.split('/')))
                        if mode == 'dates':
                            if date in student:
                                student[date] += float(v)
                            else:
                                student[date] = float(v)
                        elif mode == 'exercises':
                            if ex in student: student[ex] += float(v)
                            else: student[ex] = float(v)
            for k, v in student.items():
                if k not in data:
                    data[k] = []
                data[k].append(v)
        out = {}
        for k, v in data.items():
            out[k] = {
                'passed': np.where(np.array(v) > 0)[0].size,
                'first': np.percentile(np.array(v), 25),
                'last': np.percentile(np.array(v), 75),
                'median': np.median(np.array(v)),
                'mean': np.mean(np.array(v)),
            }
        print(json.dumps(out, indent = 4))

if __name__ == '__main__':
    main()