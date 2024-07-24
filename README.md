# Crime-Visualization-Dashboard

1. Make sure you have python version 3.10 
2. Install a virtual environment
  	- Creation: python3 -m venv mvenv
    - Activation: source venv/bin/activate
3. pip install -r requirements.txt

4. Install mongoDB docker image
    - docker pull mongo:latest
    - docker run -d -p 27017:27017 --name mongodb mongo:latest

6. Run the databse script (Do this only once)
    - Python backend/database.py

To run the Pytests go to tests directory and type
    - pytest <test name>

