## Web server storage

It's possible to use the Dropbox functionality to store snapshots or video on your own server.

Look under Motion Settings»Motion Detection»Storage»Dropbox storage. There should be an option to change the Dropbox URL. This can be set to an internal or external web server. The default uses the Dropbox server.
Example: https[]()://yourserver/dafangstor.php

[dafangstor.php](dafangstor.php) is an example PHP script that can be used on your own server. Inside this file there are two options:
 * APIKEY
 * OUTDIR

APIKEY is the Long Lived Token value that is used to authenticate requests. This must match the value entered under Settings»Motion Detection»Storage»Dropbox storage»Dropbox Long Lived Token. The PHP script can be modified to include more fancy features like maybe for example changing the OUTDIR based on the authentication token or something similar.

OUTDIR sets the output directory relative to where PHP is running. The www user (eg. www-data) will need access permissions for this directory so that it can create sub directories and output files or you can manually create directories beforehand. Paths specified by "Dropbox snapshots remote directory" and "Dropbox videos remote directory" will be relative to this OUTDIR directory.
