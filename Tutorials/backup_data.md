# Backing up data using rclone

As computational chemists, our calculations are large, necessitating the use of
high-performance computing clusters. Continuously transferring data to and from
these remote clusters is time-consuming, and possibly limited by the storage
space of your machine. To avoid this issue, we can back up data to cloud
storage directly from the remote cluster.

To do this, we can utilise the [rclone](https://rclone.org/) program, similar
in usage to `rsync` while allowing connections to cloud services.

From the official documentation, run the following command on the remote server: 

```sh
curl https://rclone.org/install.sh | sudo bash
```

You may have to change the installation paths depending on whether you have
root access. If so, redirect the shell script to a file with `curl ... > install.sh` 
and edit this directly.

Once installed, you have to configure `rclone` to connect to your choice of
cloud storage. All common storage providers are available, including
[Dropbox](https://www.dropbox.com/),
[Google Drive](https://www.google.com/drive/) and [OneDrive](https://onedrive.live.com/about/en-au/). To do this, run `rclone config`.

Then perform the following steps to link rclone to Google Drive:

1. Set up a new remote.

```
No remotes found - make a new one
n) New remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
n/r/c/s/q>
```
  Select `n`.

2. Give the name of your storage provider, which you will refer to when calling
   rclone.

```
 1 / 1Fichier
   \ "fichier"
 2 / Alias for an existing remote
   \ "alias"
 3 / Amazon Drive
   \ "amazon cloud drive"
 4 / Amazon S3 Compliant Storage Provider (AWS, Alibaba, Ceph, Digital Ocean, Dreamhost, IBM COS, Minio, etc)
   \ "s3"
 5 / Backblaze B2
   \ "b2"
 6 / Box
....
 13 / Google Drive
   \ "drive"
....
```

  Select `drive`.


3. Select a client ID. 

  Here, we can leave this field blank, so just press Enter. If you want to
improve the rate of file transfers, you can set a client ID following the
instructions [here](https://rclone.org/drive/#making-your-own-client-id).

4. Enter a client secret. 

  Leave this blank if you pressed Enter in the previous step. If you set up your
own client ID, a secret token will be provided for you to enter here.

5. Give the scope with which rclone can access your file system.

  We want rclone to write files to the Google Drive system, so type `drive` to
give rclone full access.

5. Add a root folder ID.

  Leave this blank. Press Enter.

6. Add a service account file.

  Again, leave this empty. Press Enter.

7. When asked to edit the advanced config, select `No`.

8. When asked to use auto configuration, select `No`.

9. A web link will then appear. Copy and paste this into your browser and sign
   in to the Google account you want to copy files to. 

  A verification code will appear- copy this into your terminal.



Then you are finished! When asked if all is OK, select `yes` and quit the
interactive prompt. You can now use the `rclone` command to copy files to
Google Drive.

To do so, create a folder in Google Drive called `backups`, or something
similar. Then use a script like the one below to copy files over from the
remote server to Google Drive:

```sh
#!/usr/bin/env sh

~/bin/rclone copy --update --fast-list        \
  --drive-chunk-size=1M                       \
  --filter '- *.F*'                           \
  --filter '- *tar'                           \
  --filter '- *pyc'                           \
  /full/path/to/folder/ GoogleDrive:backups/remote
```

## Important points

- The use of `rclone sync` will destroy any data you have copied over to cloud
  storage if the file is no longer present on the HPC cluster. For example, if
the HPC maintenance team have a purge policy in place, all of the data copied
over will be destroyed as soon as the remote file system is purged! So I
strongly recommend you use `rclone copy` instead.

- If you have files that you do not wish to copy over, use the `filter`
  command. In the example above, temporary files used by the
[GAMESS](https://www.msg.chem.iastate.edu/gamess/) software
are ignored, as well as compiled python byte code and large tarballs that may
not be required if the original files are copied over.


# Automating the backup process

On some Linux servers, you may be able to automate the execution of scripts
using a cron job. For a nice guide, see
[here](https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/). You can
check if you have the correct permissions by running `crontab -l`.

The syntax of a cron job is as follows:

```
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
```

Using this syntax, we can schedule a backup to occur daily, or maybe every
hour. 

To back up data daily, we can type `crontab -e` to add a command, then type

```
0 0 * * * /path/to/script.sh
```

This tells the cron utility to run script `/path/to/script.sh` at 00:00, or at
midnight each day. Alternatively, we can run the script every hour with

```
0 * * * * /path/to/script.sh
```

by telling `cron` to run the job on the hour, every hour.


# Important points

Warning: Be aware of the difference between * and 0. A command like this:

```
* * * * * /path/to/script.sh
```

will run the script every minute! As backups will most likely take a few
minutes, this will lead to multiple unfinished processes occurring
simultaneously, with the possibility of data corruption and over-use of the HPC
login nodes. NEVER run this command!

For help with scheduling cron jobs, go to the following link: [crontab guru](https://crontab.guru/)
