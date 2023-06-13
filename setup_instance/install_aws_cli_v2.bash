if ! aws --version || [ $(aws --version | grep -oE "aws[-]cli[/][0-9.]+" | cut -d "/" -f2 | cut -d "." -f1) -eq 1 ]; then
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
	unzip awscliv2.zip #&& \
	#sudo ./aws/install && \
	#rm awscliv2.zip && rm -r aws
fi
#aws-cli/1.27.71
