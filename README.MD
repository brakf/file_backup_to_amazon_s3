# S3 Backup Upload

## Purpose
This app can be used to backup certain files to an AWS S3 Storage. 5 versions of the files are kept and then deleted if older than 5 days.

## Contents:
The package contains two components:
- Terraform Code to create the S3 Bucket and setup the needed lifecycle policies and versioning as well as a technical user
- A simple python script + config file to do the work. The script should be set up to run on a schedule
