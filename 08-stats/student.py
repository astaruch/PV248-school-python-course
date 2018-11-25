from sys import argv
import csv
import json
import numpy as np
from datetime import datetime, date
from math import ceil


def main():
    filename = argv[1]
    mode = argv[2]
    with open(filename) as csv_file:
        cvs_reader = csv.DictReader(csv_file, delimiter=',')
        data = {}
        if mode == 'average':
            student_points = {}
            student_count = {}
            for row in cvs_reader:
                for k, v in row.items():
                    if k != 'student':
                        if k in student_points:
                            student_points[k] += float(v)
                            student_count[k] += 1
                        else:
                            student_points[k] = float(v)
                            student_count[k] = 1
            data['student'] = mode
            for k, v in student_points.items():
                data[k] = v / (student_count[k])
        else:
            student_id = mode
            for row in cvs_reader:
                if row['student'] == student_id:
                    data = row
        per_date = {}
        per_exercise = {}
        for k, v in data.items():
            if k != 'student':
                (date, ex) = tuple(k.split('/'))
                if date in per_date:
                    per_date[date] += float(v)
                else:
                    per_date[date] = float(v)
                if ex in per_exercise:
                    per_exercise[ex] += float(v)
                else:
                    per_exercise[ex] = float(v)
        # print(per_date)
        points = []
        dates = []
        for v in per_exercise.values():
            points.append(v)
        dates = [(k,v) for k,v in per_date.items()]
        start_date = datetime.strptime("2018-09-17",'%Y-%m-%d').date().toordinal()
        # print(points)

        d = []
        p = []
        for k, v in sorted(dates, key = lambda k: k[0]):
            p.append(v)
            d.append(datetime.strptime(k, '%Y-%m-%d').date().toordinal() - start_date)
        # print(p)

        for idx in range(1, len(p)):
            p[idx] += p[idx-1]
        d = np.array(d)
        reg= np.linalg.lstsq([[d1] for d1 in d], p, rcond=None)[0].item()
        st = {}
        st["regression slope"] = reg
        st["passed"] = np.where(np.array(points) > 0)[0].size
        st["median"] = np.median(np.array(points))
        st["mean"] = np.mean(np.array(points))
        st["total"] = np.sum(np.array(points))
        if reg != 0:
            st["date 16"] = str(datetime.fromordinal((start_date + int(16 / reg))).date())
            st["date 20"] = str(datetime.fromordinal((start_date + int(20 / reg))).date())

        print(json.dumps(st, indent=4))


        # print(p)?
        # print(d)?


        # out = {}
        # for k, v in data.items():
        #     out[k] = {
        #         'passed': np.where(np.array(v) > 0)[0].size,
        #         'first': np.percentile(np.array(v), 25),
        #         'last': np.percentile(np.array(v), 75),
        #         'median': np.median(np.array(v)),
        #         'mean': np.mean(np.array(v)),
        #     }
        # print(json.dumps(out, indent = 4))

if __name__ == '__main__':
    main()