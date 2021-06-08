#!/bin/bash	
url=$1
if [ ! -d "$url" ];then
	mkdir $url
fi

echo "[+] Harvesting subdomains with assetfinder..."
assetfinder $url | grep $1 >> $url/subs.txt
echo "done"


echo "[+] Using amass..."
amass enum -d $url >> $url/f.txt
sort -u $url/f.txt >> $url/subs.txt
rm $url/f.txt
echo "done"

echo "[+] Probing for alive domains..."
cat $url/subs.txt | sort -u | httprobe -s -p https:443 | sed 's/https\?:\/\///' | tr -d ':443' >> $url/a.txt
sort -u $url/a.txt > $url/alive.txt
rm $url/a.txt
echo "done"


echo "[+] Using aquatone...."
aquatone-discover -d $url 
awk -F ',' '{print $1}' /root/aquatone/$url/hosts.txt >> $url/alive.txt      
echo "done"


echo "[+] Using subfinder...."
subfinder -d $url -o $url/subfinder.txt > /dev/null
sort -u $url/subfinder.txt >> $url/alive.txt
echo "done"


echo "[+] Using sublist3r....."
python3 /root/tools/Sublist3r/sublist3r.py -d $url -o $url/sublist.txt > /dev/null
sort -u $url/sublist.txt >> $url/alive.txt
echo "done"


echo "[+] Removing duplicates to make a final list..."
sort -u $url/alive.txt | httpx >> $url/subdomains.txt
echo "done"
cat $url/subdomains.txt

echo "You can check the subdomains in subdomains.txt"


echo "[+] Running eyewitness against the final domains..."
python3 EyeWitness/Python/EyeWitness.py --web -f $url/subdomains.txt -d $url/eyewitness --resolve
