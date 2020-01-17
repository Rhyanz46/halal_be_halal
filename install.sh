sudo rm -r env
sudo apt install virtualenv
sleep 1s
virtualenv -p python3 env
sleep 1s
. env/bin/activate
sleep 1s
pip install -r req.txt
flask new
sudo python3 create_supervisor_conf.py
sudo supervisorctl reread
sudo service supervisor restart
echo "wait for 2 second"
sleep 2s
sudo supervisorctl status
sudo python3 create_nginx_conf.py
sudo nginx -t
sudo service nginx restart
echo "wait for 2 second"
sleep 2s
sudo service nginx status
