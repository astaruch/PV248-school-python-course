# Statistics

Statistics
- fetch points.csv from study materials
- each column is one deadline of one exercise
- each line is one student, cells are points
- an average student has average points in each column
- you can use pandas and/or numpy if you like

Bulk Stats
- invocation: ./stat.py file.csv <mode>
- <mode> is one of: dates, deadlines, exercises
- in each mode, list all such entities along with
- mean, median, first and last quartile of points
- number of students that passed (points > 0)
- the output is a JSON dictionary of dictionaries
- date YYYY-MM-DD, exercise NN, deadline YYYY-MM-DD/NN

: Individual Stats
- invocation: ./student.py file.csv <id>
- <id> is the student identiϐier or average
- output mean and median points per exercise
- a number of passed exercises and total points
- a linear regression for cumulative points in time
- keys: regression slope (intercept is 0)
- expected date to pass the 16 and 20 point marks
- keys: date 16 and date 20