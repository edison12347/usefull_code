# Initial
echo -e "general installation";
sudo apt-get update;
sudo apt-get -y upgrade;
sudo apt install -y curl;
sudo apt-get install python-pip;
sudo add-apt-repository ppa:ubuntu-desktop/ubuntu-make;
sudo apt install ubuntu-make;

# install Google Chrome browser
# echo -e "installing Google Chrome browser";
# wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -; 
# sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list';
# sudo apt-get update;
# sudo apt-get install google-chrome-stable;
# echo -e "installation complete";

# install editors
echo -e "installing editors";
	# install Atom
	#echo -e "installing Atom";
	#sudo add-apt-repository ppa:webupd8team/atom;
	#sudo apt update; 
	#sudo apt install atom;
	#echo -e "Atom installed";
	# install Sublime 3
	echo -e "installing Sublime";
	sudo add-apt-repository ppa:webupd8team/sublime-text-3;
	sudo apt-get update;
	sudo apt-get install -y sublime-text-installer;
	echo -e "Sublime installed"
	# install Pycharm (https://tecadmin.net/install-pycharm-python-ide-in-ubuntu/#)
	echo -e "installing Pycharm;"
	sudo apt-get update;
	umake ide pycharm;
	echo -e "Pycharm installed"

echo -e "editor installation complete";


# install file manager
	# install Krusader
	echo -e "installing file manager"
	sudo apt-get install -y krusader ;
	echo -e "Krusader installed"
# install docker and k8tis
echo -e "installing docker and k8tis";
	# install Docker
	sudo apt-get update;
	sudo apt-get install -y docker.io;
	sudo groupadd docker;
	sudo gpasswd -a $USER docker;
	sudo docker volume create portainer_data
	sudo docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer;
	# install Google SDK
	export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)";
	echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list;
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -;
	sudo apt-get update && sudo apt-get install google-cloud-sdk -y;
	# install Kubernetes
	sudo apt-get install -y kubectl;
	echo "source <(kubectl completion bash)" >> ~/.bashrc;
echo -e "docker and k8tis installation complete";

# install messaging apps
	# Skype Beta
	#echo -e "install Skype Beta";
	#dpkg -s apt-transport-https > /dev/null || bash -c "sudo apt-get update; sudo apt-get install apt-transport-https -y";
	#curl https://repo.skype.com/data/SKYPE-GPG-KEY | sudo apt-key add -;
	#echo "deb [arch=amd64] https://repo.skype.com/deb stable main" | sudo tee /etc/apt/sources.list.d/skype-stable.list;
	#sudo apt update;
	#sudo apt install skypeforlinux;
	# Slack Beta
	# echo -e "install Slack Beta";
	# https://slack.com/downloads/instructions/ubuntu
	
# install Django and dependencies	
	pip install django
	pip install django-autocomplete-light

