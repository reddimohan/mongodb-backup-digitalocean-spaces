#### Python and Shell script for taking MongoDB backup and upload to the DigitalOcean Spaces

###### Python Version used
```
$ python -V
Python 3.5.6 :: Anaconda, Inc.
```
Create Space in DigitalOcean
----------------------------
1. First thing first create a *Space* in the DigitalOcean cloud, Click [here](https://www.digitalocean.com/community/tutorials/how-to-create-a-digitalocean-space-and-api-key) to know how to create *Space*.
2. After creating a space, you will have **ACCESS_ID**, **SECRET_KEY** and **URL** (ex: https://nyc3.digitaloceanspaces.com/[space_name])
3. Lets create a environment variables, so that we don't expose the access and secret keys in the code

Create environment variable (Ubuntu)
------------------------------------
To set a variable you can simply run `export` command in the Terminal. ex: `export ACCESS_ID=accessid_from_digitalocean`. But this is temporary and works with only the current terminal session. To set this permanently for all the future terminal sessions we need to add export command to the `~/.bashrc` file which is located in the home directory.

Now lets add the all keys to the *.bashrc* file.
Open *.bashrc* file and add the below lines with your own keys.

`sudo -H gedit ~/.bashrc`

```
# Keys for uploading files to DigitalOcean Space
ACCESS_ID="your_access_id"
SECRET_KEY="your_secret_key"
ENDPOINT_URL="https://{}.digitaloceanspaces.com"
```
In ``ENDPOINT_URL`` you notice we have add curly braces which we will be replacing in our python script.
Execute `source ~/.bashrc` command after updating the above lines to .bashrc file and now you should be able to access this from your script/terminal.

#### Clone the repository to the machine where you have the MongoDB and want to take backup.
`git clone https://github.com/reddimohan/mongodb-backup-digitalocean-spaces.git`
Install the required python libraries used in python scripts.

Usage
-----
By executing the `backup.sh` shell file will take the backup based on current date and uploads to the DigitalOcean spaces.
```sh
sh /path/to/backup.sh school_db

snapshotting the db school_db and creating archive
2019-04-02T12:42:29.114+0530	writing school_db.results to
2019-04-02T12:42:29.114+0530	writing school_db.students to
2019-04-02T12:42:29.114+0530	done dumping school_db.results (0 documents)
2019-04-02T12:42:29.114+0530	done dumping school_db.students (0 documents)
Switching directory to /home/mohan/mongodb_backups/020419
Compressing /home/mohan/mongodb_backups/020419/school_db DB to /home/mohan/mongodb_backups/020419/school_db.tar.gz
school_db/
school_db/students.metadata.json
school_db/results.bson
school_db/students.bson
school_db/results.metadata.json
Removing school_db folder from /home/mohan/mongodb_backups/020419 Dir
Uploading /home/mohan/mongodb_backups/020419/school_db.tar.gz to cloud
*** Listing the backup files from the DigitlOcean cloud ***

file /school_db/backup_020419.tar.gz - (0 MB) stored as STANDARD

*** End ***
```

You can run this script manually or can setup cron job to automate this process.
