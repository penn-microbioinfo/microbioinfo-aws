#!/bin/bash

alias spotprice="aws --region us-east-1 ec2 describe-spot-price-history --instance-types r5ad.2xlarge --start-time=$(date +%s) --product-descriptions="Linux/UNIX" --query 'SpotPriceHistory[*].{az:AvailabilityZone, price:SpotPrice}'"
