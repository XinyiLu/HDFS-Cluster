from fabric.api import *
from fabric.operations import *
import boto.ec2
import os
import xml.etree.ElementTree as ET

conn=boto.ec2.connect_to_region("us-east-1",aws_access_key_id='AKIAJ3DQP3YORWLTITMQ',aws_secret_access_key='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')
reservation=conn.get_all_instances()
instances=[]
hostnames=[]

def getInstancesInfo(keyName):
    for reserve in reservation:
            if len(reserve.instances)==3 and reserve.instances[0].key_name==keyName:
                    for instance in reserve.instances:
                        instances.append(instance)
                    break

    for instance in instances:
        env.hosts.append('ubuntu@'+instance.public_dns_name)
    print env.hosts

def downloadHDFS():
    run('sudo apt-get update;sudo apt-get install openjdk-7-jre')
    print "java installed"
    run("export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64")
    run('wget http://mirrors.gigenet.com/apache/hadoop/common/stable/hadoop-1.2.1-bin.tar.gz')
    print "hdfs downloaded"
    run('gzip -d hadoop-1.2.1-bin.tar.gz;tar -xf hadoop-1.2.1-bin.tar')
    print "hdfs unzipped"
    dirName='/home/agnes/Downloads'
    get('~/.bashrc',dirName)
    bashFile=open(dirName+'/.bashrc','a')
    bashFile.write('export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64')
    bashFile.close()
    put(dirName+'/.bashrc','~/')
    local('rm '+dirName+'/.bashrc')
    
def addPublicKey():
    get('~/.ssh/authorized_keys','/home/agnes/')
    local('cat /home/agnes/id_rsa.pub >> /home/agnes/authorized_keys')
    put('/home/agnes/authorized_keys','~/.ssh')
    local('rm /home/agnes/authorized_keys')

def getPublicKey():
    run('ssh-keygen -t rsa -P ""')
    get('~/.ssh/id_rsa.pub','/home/agnes/')  

def connectToMaster():
    master=env.hosts[0]
    env.hosts=[master]

def formatNameNode():
    run('~/hadoop-1.2.1/bin/hadoop namenode -format')

def getHostNames():
    hostnames.append(run('hostname'))

def configFiles():
    dirName='/home/agnes/conf'
    os.mkdir(dirName)
    get('~/hadoop-1.2.1/conf/hadoop-env.sh',dirName)
    javaConf=open(dirName+'/hadoop-env.sh','a')
    javaConf.write('export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64')
    javaConf.close()
    masterConf=open("/home/agnes/conf/masters","w+")
    masterConf.write(hostnames[0]+'\n')
    masterConf.close()
    masterConf=open("/home/agnes/conf/slaves","w+")
    index=1
    while index<len(instances):
        masterConf.write(hostnames[index]+'\n')
        index+=1
    masterConf.close()
    root=ET.Element('configuration')
    propNode=ET.SubElement(root,'property')
    nameNode=ET.SubElement(propNode,'name')
    valueNode=ET.SubElement(propNode,'value')
    nameNode.text='fs.default.name'
    valueNode.text="hdfs://"+instances[0].public_dns_name+':9000'
    tree=ET.ElementTree(root)
    tree.write('/home/agnes/conf/core-site.xml')
    nameNode.text='dfs.replication'
    valueNode.text='1'
    tree.write('/home/agnes/conf/hdfs-site.xml')
    nameNode.text='mapred.job.tracker'
    valueNode.text=instances[0].public_dns_name+':54311'
    tree.write('/home/agnes/conf/mapred-site.xml')
    fileNames=os.listdir(dirName)
    for fileName in fileNames:
        put(dirName+'/'+fileName,'~/hadoop-1.2.1/conf')
    local('rm -r '+dirName)

def copyToNode():
    put('/home/agnes/test/test1.jar','~/')
    put('/home/agnes/test/pg4300.txt','~/')









