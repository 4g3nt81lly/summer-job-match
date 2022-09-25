# summer-job-match

A Django powered web application for part-time summer job matching for students.

## 🔧&ensp;Get Started.

1. Install Python 3.

 https://docs.python-guide.org/starting/install3/osx/

2. Install `django` and `pyecharts`.

 After installing Python, open Terminal:
 ```lang-shell
 pip3 install django pyecharts
 ```

3. Change to the site directory.
  ```lang-shell
  cd "/path/to/mysite"
  ```
  Replace `/path/to/mysite` with path to the site directory.

4. Update the database:
  ```lang-shell
  python3 manage.py makemigrations
  ```
If it prompts to confirm change, strike key `Y` to proceed.
  ```lang-shell
  python manage.py migrate
  ```

5. Run the test server.
  ```lang-shell
  python manage.py runserver 0.0.0.0:8888
  ```

6. Open a browser and enter "http://127.0.0.1:8888/findbestjob" in the address bar.
