# Initial
echo -e "general installation";
sudo apt-get update;
sudo apt-get upgrade -y;
sudo apt install curl -y;
sudo apt-get install python-pip;
sudo add-apt-repository ppa:ubuntu-desktop/ubuntu-make;
sudo apt install ubuntu-make;

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
	echo -e "installing Atom";
	sudo add-apt-repository ppa:webupd8team/atom;
	sudo apt update; 
	sudo apt install atom;
	echo -e "Atom installed";
	# install Sublime 3
	echo -e "installing Sublime";
	sudo add-apt-repository ppa:webupd8team/sublime-text-3;
	sudo apt-get update;
	sudo apt-get install sublime-text-installer;
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
	sudo apt-get install krusader -y;
	echo -e "Krusader installed"
# install docker and k8tis
echo -e "installing docker and k8tis";
	# install Docker
	sudo apt-get update;
	sudo apt-get install docker.io -y;
	sudo groupadd docker;
	sudo gpasswd -a $USER docker;
	# install Google SDK
	export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)";
	echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list;
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -;
	sudo apt-get update && sudo apt-get install google-cloud-sdk -y;
	# install Kubernetes
	sudo apt-get install kubectl -y;
	echo "source <(kubectl completion bash)" >> ~/.bashrc;
echo -e "docker and k8tis installation complete";

# install messaging apps
	# Skype Beta
	echo -e "install Skype Beta";
	dpkg -s apt-transport-https > /dev/null || bash -c "sudo apt-get update; sudo apt-get install apt-transport-https -y";
	curl https://repo.skype.com/data/SKYPE-GPG-KEY | sudo apt-key add -;
	echo "deb [arch=amd64] https://repo.skype.com/deb stable main" | sudo tee /etc/apt/sources.list.d/skype-stable.list;
	sudo apt update;
	sudo apt install skypeforlinux;
	# Slack Beta
	# echo -e "install Slack Beta";
	# https://slack.com/downloads/instructions/ubuntu

# install Odoo dependencies (https://www.cybrosys.com/blog/how-to-configure-pycharm-for-odoo-development-in-ubuntu)
	echo -e "install Odoo dependencies";
		sudo sh -c 'echo "deb http://archive.getdeb.net/ubuntu $(lsb_release -sc)-getdeb apps" >> 	/etc/apt/sources.list.d/getdeb.list';
		wget -q -O - http://archive.getdeb.net/getdeb-archive.key | sudo apt-key add -;
		sudo apt update;
		sudo apt install pycharm;
		sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list';
		wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -;
		sudo apt-get update;
		sudo apt-get install postgresql postgresql-contrib;
		sudo apt-get install python-dateutil python-docutils python-feedparser python-jinja2 python-ldap python-libxslt1
			python-lxml python-mako python-mock python-openid python-psycopg2 python-psutil python-pybabel python
			pychart python-pydot python-pyparsing python-reportlab python-simplejson python-tz python-unittest2 python
			vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi poppler
			utils python-pip python-pyPdf python-passlib python-decorator -y;
		sudo apt-get install gcc python-dev mc bzr python-setuptools python-babel python-feedparser python-reportlab-accel
			python-zsi python-openssl python-egenix-mxdatetime python-jinja2 python-unittest2 python-mock python-docutils
			lptools make python-psutil python-paramiko poppler-utils python-pdftools antiword -y;
		sudo curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -;
		sudo apt install -y nodejs;
		sudo apt install -y npm;
		sudo npm install -g less less-plugin-clean-css;
		sudo apt-get install python-werkzeug -y;
		sudo apt-get install python-lxml -y;
		pip2 install passlib;
		sudo apt-get install python-geoip;
		pip2 install decorator;
		pip2 install python-dateutil;
		pip2 install psycopg2;
		pip2 install pyyaml;
		pip2 install image;
		pip2 install Python-Chart;
		pip2 install reportlab;
		pip2 install prettytable Mako pyaml dateutils --upgrade;
		pip2 install psutil;
		pip2 install jinja2;
		sudo apt-get install python-docutils;
		pip2 install mock
