# Stanzaliving Assignment

## TechStack Used
1. Python (Programming Language)
2. Django (Web Framework)
3. SQLite (Database)


### How to setup and run locally
  1. Clone the Repository.
  2. Redirect to project base directory.
  3. Run the following command for installing dependencies.

    $ pip install -r requirements.txt

  4. Now direct to Fampay folder for starting the django server.

    $ cd cd stanza_living_assignment

  5. Now before running the server, we have to setup database, so run.
 
    $ python3 manage.py migrate
   
  6. Now execute the following commands

    $ python manage.py runserver


Notes:
- After running the server url to insert new ledger will be : localhost:8000/ledger/entry/ also it is a post request
- After running the server url to get all ledger entries will be : localhost:8000/ledger/info/?reference_id={reference_id}&ledger_type={ledger_type}&reference_type={reference_type}
- After running the server url to get final balance will be : localhost:8000/ledger/final/?reference_id={reference_id}&ledger_type={ledger_type}&reference_type={reference_type}


