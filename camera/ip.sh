sleep 20
hostname -I > ip.txt
python -c 'import geocoder; g = geocoder.ip("me"); print g.city; print "lat: " + str(g.lat); print "lng: " + str(g.lng)' >> ip.txt
aws s3 cp "ip.txt" s3://pi-1/$(hostname)/
