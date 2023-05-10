#### List clusters

```
pcluster list-clusters --region us-east-1
```

#### List details about a specific cluster

```
pcluster describe-cluster --region us-east-1 --cluster-name hpc-cluster
```

#### Create a new cluster
```
pcluster create-cluster -n microbioinfo-clust -c cluster-config.yaml -r us-east-1
```

#### Delete a cluster 
```
pcluster delete-cluster -n hpc-cluster -r us-east-1
```

#### Example cluster config
```
Region: us-east-1
Image:
  Os: ubuntu2004
HeadNode:
  InstanceType: t2.nano
  Networking:
    SubnetId: subnet-xxxxxxxxxxxx
  Ssh:
    KeyName: xxxxxxxxxxxxxx
Scheduling:
  Scheduler: slurm
  SlurmQueues:
  - Name: m6a
    CapacityType: SPOT
    ComputeResources:
    - Name: m6a4xlarge
      Instances:
      - InstanceType: m6a.4xlarge
      MinCount: 0
      MaxCount: 4
    Networking:
      SubnetIds:
      - subnet-xxxxxxxxxxxx
  - Name: r6a
    CapacityType: SPOT
    ComputeResources:
    - Name: r6a2xlarge
      Instances:
      - InstanceType: r6a.2xlarge
      MinCount: 0
      MaxCount: 8
    Networking:
      SubnetIds:
      - subnet-xxxxxxxxxxxx
SharedStorage:
- Name: mbi-cluster-shared-root
  MountDir: /shared-ebs
  StorageType: Ebs
  EbsSettings:
    VolumeId: vol-xxxxxxxxxxxxxxxx
    DeletionPolicy: Retain
- Name: microbioinfo-simoni-scratch
  MountDir: /scratch
  StorageType: Ebs
  EbsSettings:
    VolumeId: vol-xxxxxxxxxxxxxxxx
    DeletionPolicy: Retain
Tags:
  - Key: BillTo
    Value:  microbioinfo
```
