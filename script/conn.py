#!/usr/bin/python
import boto.ec2
import time
import sys

conn=boto.ec2.connect_to_region("us-east-1",aws_access_key_id='AKIAJ3DQP3YORWLTITMQ',aws_secret_access_key='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')
keyStr='cluster'
if len(sys.argv)>1:
    keyStr=sys.argv[1]
keyPair=conn.create_key_pair(keyStr)
keyPair.save('~/.ssh/')
securityGroup=conn.create_security_group(name=keyStr+'Group',description='security for hdfs cluster')
securityGroup.add_rule('ssh',22,22,None,None,'0.0.0.0/0',None)
securityGroup.add_rule('http',80,80,None,None,'0.0.0.0/0',None)
securityGroup.authorize('tcp',0,65535,'0.0.0.0/0')
securityGroup.authorize('udp',0,65535,'0.0.0.0/0')
reservation=conn.run_instances(image_id='ami-d0f89fb9',min_count=3,max_count=3,key_name=keyStr,security_groups=[securityGroup.name],instance_type='t1.micro')
instances=reservation.instances
print instances,reservation
for instance in instances:
    time.sleep(5)
    instance.start()
    print instance.id+'started'
    while(instance.update()!='running'):
        time.sleep(1)
print "creating instances finished"
conn.close()


