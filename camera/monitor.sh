set -e
sleep 20
hostname -I > ip.txt
python -c 'import geocoder; print geocoder.ip("me").city' >> ip.txt
aws s3 cp "ip.txt" s3://pi-1/$(hostname)/
while true
do
	gpio -g read 4 > battery.csv
	uptime -p >> battery.csv
	date >> battery.csv
	aws s3 cp "battery.csv" s3://pi-1/$(hostname)/
	sleep 60
done
