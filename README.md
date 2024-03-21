## PostgreSQL Workflow (WSL2 Enviornment)

* Change to postgres user

    ``` su - postgres ```

### From Terminal (As postgres user)

* Create a new User

    ``` createuser <user_name> ```

* Create a new Database

    ``` createdb <db_name> ```


### From psql utility (As postgres user)

* Set a password for your user

    ``` alter user <user_name> with encrypted password '<password>' ```

* Grant privileges to your user

    ``` grant all privileges on database <db_name> to <db_user> ```

* List Databases
``` \l ```

* Connect to a Databases
``` \c <db_name> ```

* List tables in a Database
``` \d ```
