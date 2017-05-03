# How to install python virtualenv

- install python 3 interpreter. If you use windows download from [python.org](https://www.python.org/) and install.
  If you use linux OS you have python 3 preinstalled in your system

- Install python 3 virtualenv accordimg to one of the next resources:
  -  [tutorial](https://tutorial.djangogirls.org/ru/django_installation/) (NO need to install django)
  -  [stackoverflow.com](http://stackoverflow.com/questions/23842713/using-python-3-in-virtualenv)
  -  [official docs](https://virtualenv.pypa.io/en/stable/installation/)

- After installation activate your virtualnenv:
  #### Linux
  ```$ source YOUR_VENV_NAME/bin/activate```
  #### Windows
  ```C:\Users\Name\Project_name> YOUR_VENV_NAME\Scripts\activate```

- After activating virtualenv from left side of your shell you will see your (YOUR_VENV_NAME). It means virtualenv works.
- To make sure run in terminal or command line:
   ```python```
   If python version is 3 you ready to go further

- In project root directory run command to install all dependencies:
  ```pip install -r requirements.txt```


- To run the project run:
```python manage.py runserver```

- After all the steps your web application will be available by address 127.0.0.1:5000
