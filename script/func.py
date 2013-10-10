from fabric.api import run
def connectToMaster():
    run('uname -a')
    
def connectToEC2():
    run('sudo apt-get update;sudo apt-get install openjdk-7-jre')
    run("export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64")
    run('wget http://mirrors.gigenet.com/apache/hadoop/common/stable/hadoop-1.2.1-bin.tar.gz')
    run('gzip -d hadoop-1.2.1-bin.tar.gz;tar -xf hadoop-1.2.1-bin.tar')
