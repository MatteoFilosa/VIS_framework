A) Steps to run the experiment (design or evaluation phase) for the first time:

1) Install the requirements running "pip install -r requirements.txt" (If you don't have pip installed, install it)
2) Create a virtual environment by running the command "python -m venv <name_of_the_virtual_environment>" in the terminal
3) Activate the virtual environment by running <name_of_the_virtual_environment>\Scripts\activate 
4) If an error appears in the console telling that the execution of Scripts is not allowed, open a Windows
Powershell terminal in admin mode and enter the command "Set-ExecutionPolicy unrestricted". This will allow the policy of scripts execution in your machine to be unrestricted, so be careful
5) In the terminal, execute the command "set FLASK_APP=server_flask.py" or " $env:FLASK_APP = "server_flask" "
6) In the terminal, execute the command "flask run"

The server should now be running in localhost. Press the key combination "CTRL+C" to interrupt it. If it is not the first time running the experiment, follow only from point 3) to point 6).

B) How to change the experiment's URL and how to change from evaluation to design phase and viceversa:

1) In the "static" folder, you can find the file "stein-config.json". Change the "systemUrl" value to the desired url  
2) In the "server_flask.py" file, in row 18, change "evaluation.html" in "design.html". This is needed in order to design the new experiment. Remember to revert this change, when the design phase is finished, in order to run the real evaluation!
3) Follow all the steps of A) if it is the first time running the design OR evaluation phase, otherwise follow only from point 3) to 6) of A)
4) The design phase should be running in localhost
5) At the end of the design phase, a new "stein-config.json" can be downloaded. Remember to place it in the "static" folder, overwriting the previous one.
6) To run the real experiment instead of the design phase, change, in the "server_flask.py" file, at row 18, "design.html" in "evaluation.html"

N.B: The "Upload" functionality does not work at the end of the evaluation phase. Instead, the file, containing the evaluation's results, can be downloaded to your machine.
