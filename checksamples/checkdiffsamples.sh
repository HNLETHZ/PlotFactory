file=diffsamples.py
numsamp=0
while read -r line; do
   numsamp=$((numsamp+1))	
done < "$file"

echo "number of samples:" $numsamp >> notuseablediff.txt
echo "number of samples:" $numsamp >> useablediff.txt

echo "number of samples:" $numsamp
echo -n "number of samples checked: "

enum=1
while read -r line; do
   signal="$line"
   checkfile=$(edmDumpEventContent $signal | grep "displacedStandAlone")
#   echo $checkfile 
#   echo $signal
   echo -n $enum
   if [ -z "$checkfile" ]; then
      echo $signal >> notuseablediff.txt
   fi
   if [ ! -z "$checkfile" ]; then
       echo $signal >> useablediff.txt
   fi
   if [ $enum -lt 10 ]; then
      echo -n -e "\b"
   fi
   if [ $enum -ge 10 -a $enum -lt 100 ]; then
      echo -n -e "\b\b"
   fi
   if [ $enum -ge 100 -a $enum -lt 1000 ]; then
      echo -n -e "\b\b\b"
   fi
   enum=$((enum+1))
done < "$file"
echo -e "\n"
