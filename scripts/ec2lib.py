import boto3
import re
import subprocess
import time

node_addr_pat = re.compile("NodeAddr[=]([0-9]+[.][0-9]+[.][0-9]+[.][0-9]+)[ ]")

class EC2Instance(object):
    def __init__(self, hostname, addr, instance_id):
        self.hostname = hostname
        self.addr = addr
        self.instance_id = instance_id

class EC2SlurmComputeInstance(EC2Instance):
    def __init__(self, hostname, addr, instance_id):
        super().__init__(hostname, addr, instance_id)
        self.resource = boto3.resource("ec2")
        self.client = boto3.client("ec2")

    
    def from_self():
        hostname = open("/etc/hostname", 'r').read().strip()
        print(hostname)
        p = subprocess.Popen(["scontrol", "show", "node", hostname], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out,err = p.communicate()
        if p.returncode != 0:
            raise OSError(err.decode("utf-8"))
        else:
            s = re.search(node_addr_pat, out.decode("utf-8"))
            if s is not None:
                node_addr = s.group(1).replace(".", "-")
                print(node_addr)
                client = boto3.client("ec2")
                q = client.describe_instances(Filters = [{"Name": "network-interface.private-dns-name", "Values": [f"ip-{node_addr}.ec2.internal"]}])
                if not "Reservations" in q or len(q["Reservations"]) > 1 or len(q["Reservations"][0]["Instances"]) != 1:
                    raise OSError
                instance = q["Reservations"][0]["Instances"][0]
                instance_id = instance["InstanceId"]
            else:
                raise ValueError("scontrol output was not parsable for NodeAddr")
        #print(q["Reservations"])
        return EC2SlurmComputeInstance(hostname, node_addr, instance_id)

    def create_local_volume(self, size=100):
        q = self.client.create_volume(AvailabilityZone = "us-east-1a", Encrypted = False, Size = size, VolumeType = "gp3", DryRun = False, TagSpecifications=[{"ResourceType": "volume", "Tags": [
            {
                "Key": "Name", 
                "Value": f"{self.hostname}-local-storage"
                }, 
            {
                "Key": "BillTo", 
                "Value": "microbioinfo"
                }, 
            {
                "Key": "VolumeGroup", 
                "Value": "PclusterComputeTempStorage"
                }
            ]}]) 

        self.local_volume_id = q["VolumeId"]
        self.volume = self.resource.Volume(self.local_volume_id)

        self.client.get_waiter("volume_available").wait(VolumeIds = [self.local_volume_id])
        self.attach_local_volume()

    def attach_local_volume(self):
        instance = self.resource.Instance(self.instance_id)
        #volume = rc.Volume(self.local_volume_id)

        resp = self.volume.attach_to_instance(
                Device = "sdd",
                InstanceId = self.instance_id
                )
        self.client.get_waiter("volume_in_use").wait(VolumeIds = [self.local_volume_id])
        time.sleep(10)
        '''
        print("Waiting 2 minutes for volume to create")
        while self.volume.state != "available":
            time.sleep(5)
            print(self.volume.state)
            self.volume.reload()
        print("Waiting 2 minutes for volume to attach")
        while self.volume.state != "in-use":
            print(self.volume.state)
            time.sleep(5)
            self.volume.reload()
        print(resp)
        '''

    def detach_local_volume(self):
        #volume = rc.Volume(self.local_volume_id)
        resp = self.volume.detach_from_instance(Force = False)
        #resp = client.detach_volume(VolumeId = self.local_volume_id)
        self.client.get_waiter("volume_available").wait(VolumeIds = [self.local_volume_id])
        '''
        print("Waiting 2 minutes for volume to detach")
        while self.volume.state != "available":
            print(self.volume.state)
            print(client.describe_volumes(Filters = [{"Name": "volume-id", "Values": [self.local_volume_id]}])["Volumes"][0])
            time.sleep(5)
            print(self.volume)
            self.volume.reload()
        print(resp)
        '''
    def delete_local_volume(self):
        self.detach_local_volume()
        tags = {k:v for (k,v) in [tuple(x.values()) for x in self.volume.tags]}
        if "VolumeGroup" in tags and tags["VolumeGroup"] == "PclusterComputeTempStorage":
            print(self.volume.state)
            self.volume.delete()
        else:
            raise OSError("Cannot delete volume because checks are not met.")
if __name__ == "__main__":
    pass
    #worker = EC2SlurmComputeInstance.from_self()
    #worker.create_local_volume(size=1)
    #worker.delete_local_volume()

