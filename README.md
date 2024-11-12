# DBMS2024_MedicalInsurance
For Database class in Fall 2024. Concept is that of a Medical Insurance Calculator and Analyzer

The Medical Insurance Analysis System is an application that takes in publicly available information and formats it into a database. It then trains this data to be able to calculate an user's estimated medical cost based on multiple factors.


Installation Details:

The following python libraries will need to be installed:
flask
xgboost
pandas
sqlalchemy
scikit-learn (contains sklearn)


Runnning Details:

To run, run run.py in the newtry folder

Then connect to the webserver that is made. By default it is localhost:5000 and can be connected to by entering the line into a web brower's navigation bar.

A site should then populate with a navigation bar that contain information, calculations, and references.

Information contains a short overview of the site and instructions on usage.

References contains links to the information related to the project.

Calculations takes in user inputs and returns an estimated medical cost based on the submitted information.
	To use this page first select the most accurate medical information in the prompts and click the calculate button.
 	A predicted medical cost will then be displayed and stored in the history.
  	The history will display the latest 5 database entries.
   	To access more of the history, history.db stores all of the previous history data and is stored in  the app folder of the newtry folder.
