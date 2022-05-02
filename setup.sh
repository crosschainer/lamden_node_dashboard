#!/bin/bash
# This will setup the whole thing
yes | sudo apt update
yes | sudo apt-get install python3.8
yes | sudo apt-get install ufw
sudo ufw allow ssh
sudo ufw allow 5432
sudo ufw enable
wget https://bootstrap.pypa.io/get-pip.py
python3.8 get-pip.py
pip3.8 install python-daemon
pip3.8 install websocket-client
pip3.8 install psycopg2-binary
yes | sudo apt install postgresql postgresql-contrib
sudo -u postgres psql -c 'create database dashboard_admin'
sudo -u postgres psql -c 'grant all privileges on database dashboard_admin to postgres;'
sudo -u postgres psql -c "create user dashboard with encrypted password 'noods'"
sudo -u postgres psql -c 'grant all privileges on database dashboard_admin to dashboard;'
sudo -u postgres psql -c 'grant all privileges on all tables in schema public to dashboard;'
sudo -u postgres psql -d dashboard_admin -f dashboard.sql
