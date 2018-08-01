sleep 20
ifconfig > ip.txt
aws s3 cp "ip.txt" s3://pi-1/
while true
do
	gpio -g read 4 > battery.csv
	uptime -p >> battery.csv
	date >> battery.csv
	aws s3 cp "battery.csv" s3://pi-1/
	sleep 60
done
