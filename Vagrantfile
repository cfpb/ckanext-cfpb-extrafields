# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "centos/6"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 6050, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8983, host: 8983, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.synced_folder ".", "/usr/lib/ckan/default/src/ckanext-cfpb-extrafields", type: "rsync", rsync__exclude: ".git/"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
      # Don't Display the VirtualBox GUI when booting the machine
      vb.gui = false

      # Customize the amount of memory on the VM:
      vb.memory = "4096"
  end

  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # TODO: Quick and dirty Bash, but should be Ansible
  config.vm.provision "shell", inline: <<-SHELL
    # Install dependencies
    yum update
    yum install -y epel-release centos-release-scl
    yum update
    yum groupinstall -y "Development Tools"
    yum install -y python27 python27-python-devel python27-python-pip python27-python-virtualenv postgresql-server postgresql-devel git libxml2 libxml2-devel libxslt-devel openldap-devel java-1.6.0-openjdk tomcat6

    # Setup PostgreSQL database
    # TODO: Update pg_hba.conf to allow md5
    sudo service postgresql initdb
    sudo service postgresql start
    su postgres -c "psql -c \"CREATE USER ckan_default WITH SUPERUSER PASSWORD 'pass';\""
    su postgres -c "psql -c \"CREATE DATABASE ckan_default WITH OWNER ckan_default;\""

    # Setup Solr
    cd /usr/src
    curl http://archive.apache.org/dist/lucene/solr/1.4.1/apache-solr-1.4.1.tgz | tar xfz -
    mkdir -p /data/solr
    cp -R apache-solr-1.4.1/example/solr/* /data/solr
    cp apache-solr-1.4.1/dist/apache-solr-1.4.1.war /data/solr/solr.war
    chown -R tomcat /data/solr
    echo '<Context docBase="/data/solr/solr.war" debug="0" privileged="true" allowLinking="true" crossContext="true"><Environment name="solr/home" type="java.lang.String" value="/data/solr" override="true" /></Context>' >> /etc/tomcat6/Catalina/localhost/solr.xml
    mkdir -p /usr/share/tomcat6/common/endorsed
    ln -s /usr/share/java/xalan-j2.jar /usr/share/tomcat6/common/endorsed/xalan-j2.jar
    #service jetty start

    # Setup CKAN
    cd ~
    mkdir -p /usr/lib/ckan/default
    source /opt/rh/python27/enable
    virtualenv-2.7 -p python2.7 --no-site-packages /usr/lib/ckan/default
    . /usr/lib/ckan/default/bin/activate
    pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.6.6#egg=ckan'
    pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt
    pip install -e /usr/lib/ckan/default/src/ckanext-cfpb-extrafields
    pip install -r /usr/lib/ckan/default/src/ckanext-cfpb-extrafields/requirements.txt
    pip install -r /usr/lib/ckan/default/src/ckanext-ldap/requirements.txt
    chown -R vagrant: /usr/lib/ckan/
    mkdir -p /etc/ckan/default
    chown -R vagrant /etc/ckan
    paster make-config ckan /etc/ckan/default/development.ini
    cp /usr/lib/ckan/default/who.ini /etc/ckan/default
    cd /usr/lib/ckan/default/src/ckan
    paster db init -c /etc/ckan/default/development.ini

    # Last Solr Stuff
    sudo mv /data/solr/conf/schema.xml /data/solr/conf/schema.xml.bak
    sudo ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /data/solr/conf/schema.xml
    sudo service tomcat6 start
    # TODO: Set debug = true
    # TODO: Set sqlalchemy.url = postgresql://ckan_default:password@127.0.0.1/ckan_default
    # TODO: Set ckan.site_url = http://localhost:8080
    # TODO: Set ckan.simple_search = 1
    # TODO: Include CKAN plugins in config

    # To use:
    # 1. In one window, run vagrant rsync-auto
    # 2. In the other, run vagrant ssh.
    # 3. In ssh, source /opt/rh/python27/enable
    # 4. Then, source /usr/lib/ckan/default/bin/activate
    # 5. pip install -e /usr/lib/ckan/default/src/ckanext-cfpb-extrafields (on any change)
    # 6. Finally, run paster serve /etc/ckan/default/development.ini
  SHELL
end
