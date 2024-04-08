aws cloudformation create-stack \
	--stack-name stack_name \
	--template-body stack_template.json \
	--parameters file://parameters.json \
	--capabilities CAPABILITY_AUTO_EXPAND

pcluster create-cluster \
	-n cluster-name \
	-r region \
	-c cluster-config.yaml
