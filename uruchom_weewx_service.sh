#!/bin/bash

var=$(sudo systemctl show -p ActiveState weewx.service)
now=$(date)
echo $now "uruchom_weewx_service.sh"
echo $now $var
if [ "ActiveState=failed" = $var ]; then
    sudo /etc/init.d/weewx start
fi