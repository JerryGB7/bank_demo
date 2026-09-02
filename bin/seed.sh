# this file handles seeding in the database with initial data for testing and development purposes
#to run this file, make sure you are in the bank_demo directory and run the following command in a GIT BASH terminal on Windows, or a Linux/Mac terminal. It will not work in a Windows command prompt.
# bash bin/seed.sh local
# bash bin/seed.sh rds

TARGET="{#1:local}"
if [ "$TARGET" == "local" ]; then

    # TODO: replace the detailed in the db url with your details
    export DATABASE_URL="postgresql+asyncpg://postgres:<your-password>@127.0.0.1:5432/bank_dev"
    PSQL_HOST="127.0.0.1"
    PSQL_DB="bank_dev"
elif ["$TARGET" == "rds"]; then
    export DATABASE_URL="postgresql+asyncpg://postgres:<your-password>@<your-rds-endpoint>:5432/bank_dev"
    PSQL_HOST="<your-rds-endpoint>"
    PSQL_DB="bank_dev"
else 
    echo "Invalid target specified. Use 'local' or 'rds'."
    exit 1
fi

echo "Seeding the database for target: $TARGET"

cd backend

python -m scripts.day3_create_tables

psql -h "$PSQL_HOST" -U postgres -d "$PSQL_DB" -f ../db/sql/seed.sql

python -m scripts.day5_seed_users

echo "seed complete for target: $TARGET"