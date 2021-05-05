#!/bin/bash

apt-get update -q
su - vagrant

echo "downloading miniconda"
wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
chmod +x miniconda.sh

echo "installing miniconda"
./miniconda.sh -b -p /home/vagrant/miniconda3
sudo chown -R vagrant:vagrant /home/vagrant/miniconda3
eval "$(/home/vagrant/miniconda3/bin/conda shell.bash hook)"

echo "Initializing miniconda"
sudo chown -R vagrant:vagrant /home/vagrant/miniconda3
export PATH="/home/vagrant/miniconda3/bin:$PATH"
echo ". /home/vagrant/miniconda3/etc/profile.d/conda.sh" >> /home/vagrant/.bashrc
conda config --add channels conda-forge

echo "Creating jupyter env"
conda create --name jupyter_env python=3.8
sudo chown -R vagrant:vagrant /home/vagrant/miniconda3
for package in jupyterhub jupyterlab nodejs nb_conda_kernels; do conda install -n jupyter_env -c conda-forge -y $package; done

echo "Creating ironhack env"
conda create --name ironhack_env python=3.8
sudo chown -R vagrant:vagrant /home/vagrant/miniconda3
for package in pandas tensorflow=2.3.0 ipykernel scikit-learn; do conda install -n ironhack_env -y $package; done
for package in fbprophet pyarrow; do conda install -n ironhack_env -c conda-forge -y $package; done

echo "Creating Jupyterhub service definition"
sudo cat << EOF > /etc/systemd/system/jupyterhub.service
[Unit]
Description=JupyterHub
After=network.target

[Service]
User=root
Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/home/vagrant/miniconda3/envs/jupyter_env/bin:/home/vagrant/miniconda3/bin"
ExecStart=/home/vagrant/miniconda3/envs/jupyter_env/bin/jupyterhub --Spawner.notebook_dir='/vagrant'

[Install]
WantedBy=multi-user.target
EOF

echo "Activating Jupyterhub service definition"
sudo systemctl daemon-reload
sudo systemctl start jupyterhub
sudo systemctl enable jupyterhub

echo "Installing MySQL"
sudo apt install -y dirmngr
sudo apt-key adv --keyserver pool.sks-keyservers.net --recv-keys 5072E1F5
echo "deb http://repo.mysql.com/apt/debian $(lsb_release -sc) mysql-8.0" | \
    sudo tee /etc/apt/sources.list.d/mysql80.list
sudo apt-get update
sudo mkdir -p /etc/mysql
sudo cat << EOF > /etc/mysql/my.cnf
[mysqld]
default_authentication_plugin=mysql_native_password
EOF
sudo apt install mysql-server -y
echo "Creating root user"
sudo mysql -u root -e 'ALTER USER "root"@"localhost" IDENTIFIED BY "root"'
sudo mysql -u root -proot -e 'CREATE USER "root"@"%" IDENTIFIED BY "root"'
sudo mysql -u root -proot -e 'GRANT ALL PRIVILEGES ON *.* TO "root"@"%" WITH GRANT OPTION'
sudo mysql -u root -proot -e 'FLUSH PRIVILEGES'

echo "Enabling remote connections"
sudo sed -i "s/^bind-address.*//" /etc/mysql/mysql.conf.d/mysqld.cnf
sudo sed -i "s/^mysqlx-bind-address.*//" /etc/mysql/mysql.conf.d/mysqld.cnf

echo "Restarting and enabing mysql service"
sudo systemctl restart mysql.service
sudo systemctl enable mysql.service

