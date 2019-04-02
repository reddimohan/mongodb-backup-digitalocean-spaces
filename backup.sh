#!/bin/sh
DIR=`date +%d%m%y`
DEST=$HOME/mongodb_backups/$DIR
TAR_FILE=$DEST/$1.tar.gz
BASEDIR=$HOME/mongodb_backup_scripts # Mongodb scripts path

DB_PASSWORD='mongodb_password'

log() {
    echo $1
}

do_backup(){
  echo 'snapshotting the db '$1' and creating archive'
  
  # Creating backup folder with current timestamp
  mkdir -p $DEST
  mongodump -d $1 -u admin -p $DB_PASSWORD --authenticationDatabase admin -o $DEST
  
  # restore db
  # mongorestore --db db_name -u admin -p $DB_PASSWORD --authenticationDatabase admin /path/to/folder/
  
  # Switching to $DEST directory to compress the snapshop of db
  log 'Switching directory to '$DEST''
  cd $DEST
  
  log 'Compressing '$DEST/$1' DB to '$TAR_FILE''
  tar -cvzf $TAR_FILE $1

  echo 'Removing '$1' folder from '$DEST' Dir'
  rm -r $1
}

save_in_cloud(){
  # Upload to Digitalocean Storage
  cd $BASEDIR
  
  # Call python script to upload
  python upload_cloud.py $1 $2
}


if [ -z $1 ] && echo "DB name Arg is missing"; then
  echo
else
  do_backup $1 && save_in_cloud $TAR_FILE $1
fi
