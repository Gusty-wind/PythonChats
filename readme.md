
This project user the python-tornado and db server use the postgres
    front end use the Jquery and emojio.js
    connect web server and db server user the fast Api.
# Python
    # pip install tornado
    # pip install simplejson
    # pip install FastAPI

# postgres 
  Install the postgres by docker
    docker run -d -p 5432:5432 \
        --name init-postgres \
        -e "ALLOW_IP_RANGE=0.0.0.0/0" \
        -e "POSTGRES_USER=admin" \
        -e "POSTGRES_PASSWORD=12345678" \
        -e "PGDATA=/var/lib/postgresql/data/pgdata" \
        -v pgdata:/var/lib/postgresql/data \
        postgres
# Porject Targets
 1. User would use it chat to one person whom he/she wanna chat. (finish)
 2. Send the image and emojio to others.(finish)
 3. User first login must regiser a account (finish)
    There are login view and register view.
    1. Check user if exist. check user password active.
    2. Save a new user data to the DB server.

# Future
    Replace the Jquery to React
    Maybe would user the mic front end skill.
    Add video
    Add send file.

