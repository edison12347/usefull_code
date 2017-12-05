# Initial
echo -e "general installation";
sudo apt-get update;
sudo apt-get -y upgrade;
sudo apt-get -y install curl ;
sudo apt-get install python-pip;
sudo add-apt-repository ppa:ubuntu-desktop/ubuntu-make;
sudo apt-get -y install ubuntu-make;

# install Google Chrome browser
 echo -e "installing Google Chrome browser";
 wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -; 
sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list';
 sudo apt-get update;
 sudo apt-get install google-chrome-stable;
 echo -e "installation complete";

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
	sudo apt-get -y install sublime-text-installer;
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
	sudo apt-get -y install krusader ;
	echo -e "Krusader installed"
# install docker and k8tis
echo -e "installing docker and k8tis";
	# install Docker
	sudo apt-get update;
	sudo apt-get -y install docker.io;
	sudo groupadd docker;
	sudo gpasswd -a $USER docker;
	sudo apt -y install docker-compose;
	sudo docker volume create portainer_data;
	sudo docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer;
	# install Google SDK
	export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)";
	echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list;
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -;
	sudo apt-get update && sudo apt-get -y install google-cloud-sdk;
	# install Kubernetes
	sudo apt-get -y install kubectl;
	echo "source <(kubectl completion bash)" >> ~/.bashrc;
echo -e "docker and k8tis installation complete";

# upgrade terminal\
	#echo -e "upgrade terminal";
	#sudo apt-get install zsh;
	#sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# install messaging apps
	# Skype Beta
	echo -e "install Skype Beta";
	dpkg -s apt-transport-https > /dev/null || bash -c "sudo apt-get update; sudo apt-get install apt-transport-https -y";
	curl https://repo.skype.com/data/SKYPE-GPG-KEY | sudo apt-key add -;
	echo "deb [arch=amd64] https://repo.skype.com/deb stable main" | sudo tee /etc/apt/sources.list.d/skype-stable.list;
	sudo apt update;
	sudo apt-get -y install skypeforlinux;
	# Slack Beta
	echo -e "install Slack Beta";
	https://slack.com/downloads/instructions/ubuntu
# install Python related
    sudo apt-get install python-dev   # for python2.x installs
    sudo apt-get install python3-dev  # for python3.x installs

# install Django and dependencies	
	pip install django
	pip install django-autocomplete-light

# install Photo editors	
	echo -e "install Gimp";
	sudo apt-get -y install gimp;
	echo -e "install DarkTable";
	sudo apt-get -y install darktable;


