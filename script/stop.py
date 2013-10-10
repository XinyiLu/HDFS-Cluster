#!/usr/bin/python
import boto.ec2
import sys

conn=boto.ec2.connect_to_region("us-east-1",aws_access_key_id='AKIAJ3DQP3YORWLTITMQ',aws_secret_access_key='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')
reservations=conn.get_all_instances()
reservation=None
for reserve in reservations:
    if reserve.instances[0].key_name==sys.argv[1]:
        reservation=reserve
        break

instances=reserve.instances
for instance in instances:
    instance.stop()
    print instance.id+" is stopped"
conn.close()
