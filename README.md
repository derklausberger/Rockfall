# Rockfall
This is a statistic flask application....

----

Requirements:
- you need pip installed on your personal computer

----

Installation:
- clone this repository to your local storage
- install required packages using the following command:
    pip install -r requirements.txt

----

Execution:
- execute the flask application using the following command:
    flask run
- open localhost in your browser on port 5000
    http://127.0.0.1/5000
- Login:
  username: admin
  password: pw

have fun!

----

Errors that need to be corrected:
- bug with the date selector: is not working (should be a minor fix - previously worked)
- bug with multiple date selectors: dynamic generation of date selectors should be excluded from the loop in plot.html
- bug with the cycle table: does not show cycle data (previously worked)

Suggestions for improvement:
- update the starting page with a small introduction
- update the loading animation to see the upload status (to make it more user-friendly)
- add user registration and set a user database up
- add file deletion for each file
- change the upload behavior of a file to replace the whole dataset and not to add it? (depends on the datasets)
- add comments, update project structure and split up files (code refactoring)
