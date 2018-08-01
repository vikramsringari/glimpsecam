sleep 30
ifconfig > ip.txt
aws s3 cp "ip.txt" s3://pi-1/
while true
do
	gpio -g read 4 > battery.log
	echo "; " >> battery.log
	uptime -p >> battery.log
	aws s3 cp "battery.log" s3://pi-1/
	sleep 60
done
