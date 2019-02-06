file="data.py"
num=0
echo "from collections import OrderedDict"

while IFS= read -r line; do
   if [[ "$line" == "#"*  ]] ; then
       echo "$line"
       echo "bkg$num = OrderedDict()"
   elif [[ "$line" != "#"* && "$line" != "" ]] ; then
       echo -n "bkg$num['$line'] = ('$line','"   
       parent= dasgoclient -query="parent dataset=$line"
   else 
       echo ""
       num=$((num+1))
   fi
done < "$file"

#
