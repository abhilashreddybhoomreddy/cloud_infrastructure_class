from fabric.api import hosts, local, run, cd, env, put

master = [
    "root@138.197.127.60",
    ]

workers = [
    "root@104.236.125.222",
    "root@138.197.28.237",
    "root@138.197.37.77",
    ]

@hosts(master+workers)
def install_packages():
    run("echo Install packages...")

    # update the repositories
    run("apt-get -y update")
    run("apt-get -y upgrade")

    # get additional packages
    run("apt-get install -y apt-transport-https")

    # add the kubernetes locations
    run("curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -")
    run("echo \"deb http://apt.kubernetes.io/ kubernetes-xenial main\"" + 
        " > /etc/apt/sources.list.d/kubernetes.list") 
    run("apt-get -y update")

    #install remaining packages
    run("apt-get install -y docker.io")
    run("apt-get install -y kubelet kubeadm kubectl kubernetes-cni")

@hosts(master)
def setup_master():
    # initialize the cluster
    run("echo Setup master...")
    run("kubeadm init --pod-network-cidr 10.244.0.0/16")
    # if you want master to run pods
    # run("kubectl taint nodes --all dedicated-")

@hosts(master)
def setup_network():
    # start pod networking
    run("echo Setup network...")
    put("kube-flannel.yml","kube-flannel.yml")
    run("kubectl apply -f kube-flannel.yml")

@hosts(master)
def confirm_network():
    # start pod networking
    run("echo Confirm network...")
    run("kubectl get pods --all-namespaces")

@hosts(workers)
def setup_workers():
    # update worker machine to join cluster
    run("kubeadm join --token=036056.a7c5cf4a4e8455b6 138.197.127.60")

@hosts(master)
def confirm_workers():
    # confirm workers
    run("echo Confirm workers...")
    run("kubectl get nodes")


