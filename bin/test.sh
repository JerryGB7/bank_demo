set -e

echo "== BANK DEMO TEST SCRIPT =="

# this script is to activate the backend virtual environment and run the tests in the tests folder
cd backend

source .venv/Scripts/activate

# checks to see if a database called bank_test exists, and if it does, it drops it. Then it creates a new database called bank_test.
psql -U postgres -c "DROP DATABASE IF EXISTS bank_test;"
psql -U postgres -c "CREATE DATABASE bank_test;"

#then we will used pytest to run the tests in the tests folder, and we will use the -v flag to get more detailed output, and we will use the --disable-warnings flag to disable warnings, and we will use the --maxfail=1 flag to stop after the first failure.
pytest -v --disable-warnings --maxfail=1 tests/test_auth.py