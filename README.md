
# Yobanco

A basic banking system that will definitely be developed in the future.

## How to run

To run Yobanco in development mode; Just use steps below:

1. Install `python3`, `pip`, `virtualenv` in your system.
2. Clone the project `[text](https://github.com/hosseinboostanchi/yobanco.git)`.
3. Make development environment ready using commands below;

  ```bash
  git clone `[text](https://github.com/hosseinboostanchi/yobanco.git)` && cd Yobanco
  virtualenv -p python3 build  # Create virtualenv named build
  source build/bin/activate
  pip install -r requirements.txt
  mv Yobanco/settings.py
  python manage.py migrate  # Create database tables
  ```

4. Run `Yobanco` using `python manage.py runserver`
5. Go to `[text](http://127.0.0.1:8000/)` to see your Yobanco version.

## Run On Windows

If You're On A Windows Machine , Make Environment Ready By Following Steps Below:
1. Install `python3`, `pip`, `virtualenv` 
2. Clone the project using:  `git clone `[text](https://github.com/hosseinboostanchi/yobanco.git)`.
3. Make Environment Ready Like This:
``` Command Prompt
cd Yobanco
virtualenv -p "PATH\TO\Python.exe" build # Give Full Path To python.exe
build\Scripts\activate # Activate The Virutal Environment
pip install -r requirements.txt
move Yobanco/settings.py
python manage.py migrate # Create Database Tables
```
4. Run `Yobanco` using `python manage.py runserver`
5. Go to `[text](http://127.0.0.1:8000/)` to see your Yobanco version.


[http://127.0.0.1:8000/]: http://127.0.0.1:8000/
