sleep 20
hostname -I > ip.txt
python -c 'import geocoder; print geocoder.ip("me").city' >> ip.txt
aws s3 cp "ip.txt" s3://pi-1/$(hostname)/
