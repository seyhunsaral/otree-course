oTree Ubuntu Server Setup
-------------------------
This is a step-by-step guide for setting up `oTree` on an `Ubuntu` server. This is, of course, not the only way to install oTree on a server and it involves several personal choices but I believe it might be helpful.


# Components
* oTree running on `Django`
* Postgresql (Database)
* Redis (Data cache)
* Supervisor (Manages oTree)

## Step 0 - Install necessary packages
These include

* Python and related packages(`python3.8-dev`, `python3-pip`)
  * Database (Postgresql) and related packages (`libpq-dev`, `postgresql-contrib`, `redis-server`). We will install them with a single command below but before that a note about python version.

* You should install a supported python version  
When I am writing this, oTree was supporting Python3.7 or 3.8. You should take a look at the "Installation" chapter. Note that I found the information only on the "MacOS" installation section. So you might want to dig a little bit to find the right version: 
https://otree.readthedocs.io/en/latest/install-macos.html#install-macos

* Update the package list 
```
sudo apt update
```

* Install necessary packages:

```
sudo apt-get install python3.8 python3.8-dev python3.8-venv libpq-dev postgresql postgresql-contrib redis-server python3-pip build-essential libssl-dev libffi-dev 
```


## Step 1 - Set up postgresql

* Switch to the postgres user

```
sudo su - postgres
```

You will see that the left side of your commmand line will be changed to `postgres@yourcomputername`

* Start the Postgres shell

```
psql
```



* * You will see that you are switched to Postgresql shell as on the left of the cursor you will see `postgres=#`

Create the database and set a password and quit Postgresql shell and switch back to your user. (Do not forget the semicolons(`;`) at the end of first two commands. They are sql commands and they require those semicolons to indicate that the command has finished)
Replace the `dbpasswordhere' string with a password you create, keeping the quotation marks enclosing the password.

```
CREATE DATABASE django_db;
alter user postgres password 'dbpasswordhere';
\q
exit
```

