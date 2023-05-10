import ec2lib

worker = ec2lib.EC2SlurmComputeInstance.from_self()
worker.create_local_volume(size=250)

