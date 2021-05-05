# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Set machine name and machine hostname
  config.vm.define "ironhackvm"
  config.vm.hostname = "ironhackvm"
  
  # User ubuntu 20.04
  config.vm.box = "ubuntu/focal64"

  # Forwarded port for Jupyter Hub
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  
  # Forwarded port for MySQL
  config.vm.network "forwarded_port", guest: 3306, host: 3306

  config.vm.provider "virtualbox" do |vb|

	 # Set machine memory to 4GB
     vb.memory = "4096"

   end

  # Set provisioning script
  config.vm.provision "shell", path: "provision.sh"
end
