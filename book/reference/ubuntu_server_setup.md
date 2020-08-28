# oTree Ubuntu Server Setup

This is a step-by-step guide for setting up `oTree` on an `Ubuntu` server. This is, of course, not the only way to install oTree on a server and it involves several personal choices but I believe it might be helpful to some people.


## Components
* oTree running on `Django`
* Nginx (Web server for reverse proxy)
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


* You will see that you are switched to Postgresql shell as on the left of the cursor you will see `postgres=#`

Create the database and set a password and quit Postgresql shell and switch back to your user. (Do not forget the semicolons(`;`) at the end of first two commands. They are sql commands and they require those semicolons to indicate that the command has finished)
Replace the `dbpasswordhere' string with a password you create, keeping the quotation marks enclosing the password.

```
CREATE DATABASE django_db;
alter user postgres password 'dbpasswordhere';
\q
exit
```
* Add `DATABASE_URL` and `REDIS_URL` enviroment variables on your `~/.bashrc`. You can use `nano` or your favourite text editor. To use nano write
```
nano ~/.bashrc
```
and add these lines to the file (replacing `dbpasswordhere` and `adminpasshere`. You can select your own admin password.

```
export DATABASE_URL=postgres://postgres:dbpasswordhere@localhost/django_db
export REDIS_URL=redis://localhost:6379
export OTREE_ADMIN_PASSWORD="adminpasswordhere"
export OTREE_PRODUCTION="1" # can set to 1                $
export OTREE_AUTH_LEVEL="STUDY" # can set to STUDY or DEMO$
```

If you are new to nano, you should at the end of your file and paste the lines above (with the password in the designated area). Press `Ctrl+O` to save the file and `Ctrl + X` to exit `nano`.

When you are done, source the code `.bashrc` file so the changes you made will be loaded.

`source ~/.bashrc`

## Step 2 - oTree Installation


* Create a virtual environment  

```
python3.8 -m venv venvotree
```

* Activate the virtual environment

```
source ~/venvotree/bin/activate
```

Add this line to the ~/.bashrc file as well so each time terminal runs, also the virtual enviroment runs. After that source ~/.bashrc file.

```
source ~/.bashrc
```
We will need to do that before trying otree because the enviromental variables we defined there earlier are necessary for oTree to run.

You should be seeing (venv) on the left side of the screen.

* Install wheel  `pip install wheel`


* Install oTree python package
```
pip install -U otree
```

* Create oTree project folder 
```
otree startproject oTree
```

* Go to the folder and install requirements 
```
cd oTree
pip install -r requirements.txt 
```

* You can run the server with `otree prodserver 8000` command. That's where the oTree will run. however before that, to test it over http, you can run it like this:

```
sudo -E env "PATH=$PATH" otree prodserver 80
```

Then you should be able to reach oTree from your browser

You might(actuall should) get a "database not ready error". in this case try 
```
otree resetdb
```

and then run the server again.


## Step 3 - Install nginx

* Install nginx
```
sudo apt install nginx
```
* Check the status
```
systemctl status nginx
```

* Allow firewall to Nginx
```
sudo ufw allow 'Nginx Full' 
sudo ufw allow ssh
sudo ufw allow 'OpenSSH'
sudo ufw enable
```

* You might not run oTree server on the port 80 when you run it from the browser after you enable ufw. This is alright as nginx will be the reverse proxy for that. Nevertheless you can stop nginx by `sudo service nginx stop`

Test the nginx invitation by going to c101-038.cloud.gwdg.de (not /demo). Sometimes oTree's redirection to /demo/ page staty in the cache. If yo usee that the hostname link you write is directed to /demo/ you can delete the cache or basically open a private browser and try there.

* Unlink the default website
```
sudo unlink /etc/nginx/sites-enabled/default
```


Create the reverse proxy file:
```
sudo nano /etc/nginx/sites-available/reverse-proxy.conf
```

with the contents (do not forget to replace the server_name `YOURHOSTNAMESHOULDBEHERE`):

```
map $http_upgrade $connection_upgrade {
    default upgrade;
        '' close;
	} 


server {
        access_log /var/log/nginx/reverse-access.log;
        error_log /var/log/nginx/reverse-error.log;

	server_name YOURHOSTNAMESHOULDBEHERE;

	location ^~/_static/{
	root /home/cloud/oTree/;
	include /etc/nginx/mime.types;
	}

	location / {
	   proxy_buffering off;
	   proxy_pass http://localhost:8000;
	   proxy_http_version 1.1;
	   proxy_set_header Upgrade $http_upgrade;
	   proxy_set_header Connection $connection_upgrade; 
	   proxy_set_header HOST $host;
	   proxy_set_header X-Real-Ip $remote_addr;
	   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	   proxy_set_header X-Forwarded-Host $server_name;
	   proxy_set_header X-Forwarded-Proto $scheme;
	   proxy_set_header X-Forwarded-Port $server_port;
	   }

}


```


* Create link to the enabled site
```
sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
```

* Check config test nginx
```
sudo service nginx configtest
```
* Restart nginx 
```
sudo service nginx restart
```


* Run oTree server 

```
sudo -E env "PATH=$PATH" otree prodserver 8000
```

and check if it worked by going to your server's url from your browser. You should be seeing oTree admin panel. If everything seems okay, stop the server and we will automatize the process using `supervisor`.



## Step 4 - Set up Supervisor 

* Install supervisor

```
sudo apt install supervisor
```
* Start supervisor 
```
sudo service supervisor start
```

* Create supervisor config for otree
```
sudo nano /etc/supervisor/conf.d/otree.conf
```

```
[program:otree]
command=/home/cloud/venvotree/bin/otree runprodserver 8000
directory=/home/cloud/oTree
stdout_logfile=/home/cloud/otree-supervisor.log
stderr_logfile=/home/cloud/otree-supervisor-errors.log
autostart=true
autorestart=true
environment=
  PATH="/home/cloud/venvotree/bin/:%(ENV_PATH)s",
  DATABASE_URL="postgres://postgres:dbsappwordhere@localhost/django_db",
  REDIS_URL="redis://localhost:6379",
  OTREE_ADMIN_PASSWORD="adminpasswordhere",
  OTREE_PRODUCTION="1", # can set to 1                                                           
  OTREE_AUTH_LEVEL="STUDY", # can set to STUDY or DEMO 
```



* Reread supervisor 
```
sudo supervisorctl reread
```


* Note: If you see such an error on supervisor reread

```
No such file or directory: file: /usr/lib/python2.7/socket.py line: 228
```
it means that supervisor is not running. Try to figure our what's wrong and run again.

* Restart supervisor
```
sudo service supervisor restart
```

## Step 5 - Using secure connection (https) by installing ssh (optional)
We will use self signed Let's encrypt

* Add repo
```
sudo add-apt-repository ppa:certbot/certbot
```

* install certbot for nginx
```
sudo apt install python-certbot-nginx
```

* Create the certificate
```
sudo certbot --nginx -d yourhostnamehere
```

When it asks
```
Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.

1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
- - - - - - - - - - - - - - 
```

Choose 2

* Restart nginx
```
sudo service nginx restart
```
Your server is ready!
