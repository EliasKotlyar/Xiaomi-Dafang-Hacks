<?php
/* A simple Dropbox-like API for your own server
   Copyright (C) 2021 Chris Osgood

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

   ##### CONFIG ###############################################################

   # Change this to some random long password.
   # This key should match the key under Settings->Motion Settings->Storage->Dropbox storage->Dropbox Long Lived Token.
   $APIKEY = "aw4QrDrz5Z94oyaYLx9ojh8ZDARt7tA8hRqosNG305shGD6NJtAcjOC3WS3odsBMdkPFvl0hJSZyIkCJ";

   # This is the directory where all images and video will be stored. Missing subdirectories will be created here
   # based on the values of "Dropbox snapshots remote directory" and "Dropbox videos remote directory".
   # Make sure the web user has access permissions for this directory.
   $OUTDIR = "/media/securitycam";

   ############################################################################

   if (!array_key_exists('HTTP_AUTHORIZATION', $_SERVER) || !array_key_exists('HTTP_DROPBOX_API_ARG', $_SERVER))
   {
      header("HTTP/1.1 500 Internal Server Error");
      error_log("ERROR: Missing authorization or API argument");
      exit();
   }

   if ($_SERVER['HTTP_AUTHORIZATION'] != "Bearer $APIKEY")
   {
      header("HTTP/1.1 403 Forbidden");
      exit();
   }

   $path = json_decode($_SERVER['HTTP_DROPBOX_API_ARG'], true);

   if ($path == null || !array_key_exists('path', $path))
   {
      header("HTTP/1.1 500 Internal Server Error");
      error_log("ERROR: Missing or bad file path `".$_SERVER['HTTP_DROPBOX_API_ARG']."'");
      exit();
   }

   $path = $path['path'];

   #----------- PATH SANITIZING -----------------------

   # Only allow basic characters and digits
   $path = str_replace("\\", "/", $path);
   $path = preg_replace("([^a-zA-Z\d \-_./])", "_", $path);

   # Clean beginning of path
   $path = preg_replace("(^[/.]+)", "", $path);

   # No path backwards; NOTE: this is a simplistic approach that will
   # disallow any paths with multiple repeating periods.
   $path = preg_replace("(\.+)", ".", $path);

   # Clean repeated path seperators
   $path = preg_replace("(\/+)", "/", $path);

   # Remove all "current directory" paths
   do {
      $oldpath = $path;
      $path = str_replace("/./", "/", $path);
   } while ($path != $oldpath);

   #---------------------------------------------------

   $dirname = dirname($path);
   $filename = basename($path);

   if (strlen($filename) < 1)
   {
      header("HTTP/1.1 500 Internal Server Error");
      error_log("ERROR: Bad file path");
      exit();
   }

   $dirname = "$OUTDIR/$dirname";
   $filename = "$dirname/$filename";

   if (!is_dir($dirname))
   {
      if (!mkdir($dirname, 0777, true))
      {
         header("HTTP/1.1 500 Internal Server Error");
         error_log("ERROR: Failed to create output directory `$dirname'");
         exit();
      }
   }

   if (file_exists($filename))
   {
      header("HTTP/1.1 500 Internal Server Error");
      error_log("ERROR: Output file already exists `$filename'");
      exit();
   }

   if (!($fp = fopen($filename, "wb")))
   {
      header("HTTP/1.1 500 Internal Server Error");
      error_log("ERROR: Failed to create output file `$filename'");
      exit();
   }

   $data = file_get_contents('php://input');
   $numbytes = fwrite($fp, $data);
   fclose($fp);

   if (!$numbytes)
   {
      header("HTTP/1.1 500 Internal Server Error");
      error_log("ERROR: Failed to write output file `$filename'");
      exit();
   }
?>
