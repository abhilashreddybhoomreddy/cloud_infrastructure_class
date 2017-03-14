from fabric.api import local, run, cd, env

#env.hosts = ["root@45.55.151.79", "greg@ssh.pythonanywhere.com"]
env.hosts = ["root@45.55.151.79"]

def install_apt_get_packages():
    run("apt-get -y update")
    run("apt-get -y upgrade")
    run("apt-get install -y python3")
    run("apt-get install -y python3-pip")
    run("apt-get install -y git")

def install_pip3_packages():
    run("pip3 install --upgrade pip")
    run("pip3 install bottle")

def install_source_code():
    run("git clone https://github.com/gregdelozier/bottle_example")

def install_server():
    install_apt_get_packages()
    install_pip3_packages()
    install_source_code()
    
def start_server():
    with cd("bottle_example"):
        run("nohup python3 main.py && sleep 10")

def ls():
    local("ls -l")

def simplels():
    run("ls -l")

def remotels():
    with cd("/"):
        run("ls -l")

def hello():
    print("hello")

def goodbye():
    print("goodbye")

def greetings():
    hello()
    goodbye()
