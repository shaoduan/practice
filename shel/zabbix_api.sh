#!/bin/bash

################################# Argument ############################
[ -f '/usr/local/bin/jshon' ] || exit 2
zabbix_url='https://zabbixserver_hostname/api_jsonrpc.php'

################################# Function ###########################
Get_Token(){
local url=${zabbix_url}
local zabbix_user=''
local password=''
#te=$(echo  "{\"jsonrpc\": \"2.0\", \"method\": \"user.login\", \"params\": {\"user\": \"${zabbix_user}\",\"password\": \"${password}\"}, \"id\": 1, \"auth\": null}")
local token=''
token=$( curl -s -k -X POST -H 'Content-Type: application/json' -d "{\"jsonrpc\": \"2.0\", \"method\": \"user.login\", \"params\": {\"user\": \"${zabbix_user}\",\"password\": \"${password}\"}, \"id\": 1, \"auth\": null}" ${url} | /usr/local/bin/jshon -Q -e result)
if [ -z "${token}" ]
then
    echo "[ Error ]: Can Not Retrieve Auth Token."
    exit 2
fi
eval $1="${token}"
}

Get_HostId(){
local url=${zabbix_url}
local auth_token="$1"
local host="$2"
local id=''
id=$( curl -s -k -X POST -H 'Content-Type: application/json' -d "{\"jsonrpc\": \"2.0\", \"method\": \"host.getobjects\", \"params\": {\"output\": \"extend\",\"name\": \"${host}\"}, \"auth\": \"${auth_token}\", \"id\":1 }" ${url} |  /usr/local/bin/jshon -Q -e result -e 1 -e hostid )
if [ -z "${id}" ]
then
    echo "[ Error ]: Can Not Retrieve Host ID Of ${host}."
    exit 2
fi
eval $3=${id}
}

Get_ItemId(){
local url=${zabbix_url}
local auth_token="$1"
local host_id="$2"
local item_name="$3"
local itemId=''
itemId=$( curl -s -k -X POST -H 'Content-Type: application/json' -d "{\"jsonrpc\": \"2.0\", \"method\": \"item.get\", \"params\": {\"output\": \"extend\",\"hostids\": \"${host_id}\", \"search\": {\"key_\": \"${item_name}\"} }, \"auth\": \"${auth_token}\", \"id\":1 }" ${url} |  /usr/local/bin/jshon -Q -e result -e 0 -e itemid )
if [ -z "${itemId}" ]
then
    echo "[ Error ]: Can Not Retrieve Item:\"${item_name}\" ID Of ${machine}."
    exit 2
fi
eval $4=${itemId}
}

Get_Value(){
local url=${zabbix_url}
local auth_token="$1"
local itemId="$2"
local begin="$3"
begin=$(/bin/date -d "${begin}" +%s)
local end="$4"
end="$(/bin/date -d "${end}" +%s)"
local data=$( curl -s -k -X POST -H 'Content-Type: application/json' -d "{\"jsonrpc\": \"2.0\", \"method\": \"history.get\", \"params\": {\"output\": \"extend\",\"history\": ${history_type:-3},\"itemids\": \"${itemId}\", \"limit\": 120, \"time_from\": ${begin}, \"time_till\": ${end}, \"sortfield\": \"clock\", \"sortorder\": \"DESC\" }, \"auth\": \"${auth_token}\", \"id\":1 }" https://beta.monitor.moshou.ruiwangame.net/api_jsonrpc.php )


local lenth=$(echo ${data} | /usr/local/bin/jshon -Q -e result -l)
lenth=$[lenth-1]
for i in $(seq -s ' ' 0 ${lenth})
do
    local value=$(echo ${data} | /usr/local/bin/jshon -Q -e result -e $i -e value  | sed -ne 's#"\(.*\)"#\1#p')
    local timestamp=$(echo ${data} | /usr/local/bin/jshon -Q -e result -e $i -e clock  | sed -ne 's#"\(.*\)"#\1#p')
    local dtime_fmt=$(/bin/date -d @${timestamp} '+%Y-%m-%d %H:%M:%S')
    echo "${dtime_fmt}  ${value}"
done
}

Usage(){
echo "
Usage:
      $(basename $0) --m "ali-moshou01-01-all-in-one_120.24.74.103" --k "net.if.in[eth1]" --begin "2015-06-02 10:24:00" --end "2015-06-02 10:26:00" --type 3

Type Values: 
  0 - float; 
  1 - string; 
  2 - log; 
  3 - integer; 
  4 - text. 
"

}
############################# Main #################################

[ $# -le 8 ] && Usage && exit 9

while [ ! -z "${1}" ]
do
    case "${1}" in
    --m)
         shift 1; machine="${1}" ; [ ! -z "$(echo ${machine} | grep '\--')" ] && shift 1 && { echo "[ Error ]: Input machine wrong" ; exit 9; }
         shift 1;;
    --k)
         shift 1; key="${1}" ; [ ! -z "$(echo ${key} | grep '\--')" ] && shift 1 && { echo "[ Error ]: Input key wrong" ; exit 9; }
         shift 1;;
    --begin)
         shift 1; btime="${1}" ; date -d "${btime}" > /dev/null 2>&1 || { shift 1 ; echo "[ Error ]: Input begin time error"; exit 9 ;}
   shift 1;;
    --end)
         shift 1; etime="${1}" ; date -d "${etime}" > /dev/null 2>&1 || { shift 1 ; echo "[ Error ]: Input end time error"; exit 9 ;}
         shift 1;;
    --type)
         shift 1; history_type="${1}" ; [ ! -z "$(echo ${history_type} | grep '\--')" ] && shift 1 && { echo "[ Error ]: Type value  wrong" ; exit 9; }
         shift 1;;
  *) 
   Usage ; exit 9 ;;
    esac
done

Get_Token 'auth_token'
#echo ${auth_token}
#auth_token='016032aa8228a023766fefc635e44868'
Get_HostId "${auth_token}" "${machine}" "host_id"
#echo ${host_id}
Get_ItemId "${auth_token}" "${host_id}" "${key}" item_id
#item_id='27298'
#echo ${item_id}
#echo 
Get_Value "${auth_token}" "${item_id}" "${btime}" "${etime}"
echo 
