# Catalog Item Project

This _**catalog_app.py**_ web application provides a list of books within a variety of categories and 
integrates Google and Facebook registration and authentication.  Authenticated users have the ability to
create, update and delete their own items.  Users that are not authenticated will only be able to view
the list of categories and the books under each category.

Requirements
* You have Python 2.7 installed on your computer
* You successfully installed Vagrant
* You successfully installed VirtualBox

# Resources

## Download the Repository
The repository contains all the necessary files to run the application.
You can download this repository to your local machine.



# Installation
You will need to perform the following operations for the application to work successfully:

* Install VirtualBox
* Install Vagrant

## Installing VirtualBox

VirtualBox is the program that runs your Linux virtual machine. [Install_it_from_this_site](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1). 
Install the _platform package_ for your operating system. You do not need the extension pack or the SDK. 
You do not need to launch VirtualBox after installing it.

## Installing Vagrant

Vagrant is the program that will download a Linux operating system and run it inside the virtual machine. [Install_it_from_this_site](https://www.vagrantup.com/downloads.html).
Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

## Bringing up the virtual machine

Vagrant takes a configuration file called `Vagrantfile` that tells it how to start your Linux VM. Using 
your terminal, change the directory (with the cd command) to the vagrant directory inside the repository
you downloaded, then run vagrant up. You should see some lines like the following:

```
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'bento/ubuntu-16.04-i386' is up to date...

```

The VM is linked to the directory where you ran `vagrant up` or 
`winpty vagrant up`(Git Bash on Windows).

To log into the VM, use a terminal in that same directory and run `vagrant ssh` or 
`winpty vagrant ssh`(Git Bash on Windows). You'll then see something like this:

```
Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.4.0-75-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


The shared directory is located at /vagrant
To access your shared files: cd /vagrant
Last login: Thu Mar 15 22:19:07 2018 from 10.0.2.2
vagrant@vagrant:~$

```

# Run the program

Once you have downloaded the repository, in your terminal change to that directory:

1. In your terminal, type `cd vagrant` 
2. Next, type `ls`, to see the `Vagrantfile` and the following directories: catalog, forum and tournament. 
3. Type `vagrant up` (reference 'Bringing Up the Virtual Machine' section above)
4. Type `vagrant ssh`
5. At `vagrant@vagrant:~$` prompt, type `cd /vagrant`
6. At `vagrant@vagrant:/vagrant$` prompt, type `cd catalog` to enter the catalog directory.
7. At `vagrant@vagrant:/vagrant/catalog$` prompt, type `python initial_data.py` to load initial data for application.
8. Next, type `python catalog_app.py`.
9. Press the `ENTER` key to run the program.
10. Open a browser window and type in the url `http://localhost:5000/`
11. Press the `ENTER` key to open the web application
12. To stop the program, in your terminal type `CTRL + C`
13. To close the VM type `vagrant halt` or `winpty vagrant halt` (Git Bash on Windows).
14. To access categories via JSON API endpoint, type `http://localhost:5000/categories/JSON` in broswer and press `ENTER`
15. To access a list of books in a particular category via JSON API endpoint, type `http://localhost:5000/category/<category id>/books/JSON` and press `ENTER`
16. To access a specific book in a particular category via JSON API endpoint, type `http://localhost:5000/category/<category id>/book/<book id>/JSON` and press `ENTER`
