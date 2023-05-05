# List clusters

```
pcluster list-clusters --region us-east-1
```

# List details about a specific cluster

```
pcluster describe-cluster --region us-east-1 --cluster-name hpc-cluster
```

# Create a new cluster
```
pcluster create-cluster -n microbioinfo-clust -c cluster-config.yaml -r us-east-1
```

# Delete a cluster 
```
pcluster delete-cluster -n hpc-cluster -r us-east-1
```
