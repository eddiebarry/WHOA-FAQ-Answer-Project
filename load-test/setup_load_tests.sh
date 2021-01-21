#!/bin/bash
for filename in ./*.py; do
    # extract host
    temphost=$(grep '# host' $filename)
    temphost=${temphost/'# host='/''}
    onlyname=${filename/'.py'/''}
    onlyname=${onlyname:2}
    onlyname=${onlyname/'_'/'-'}
    onlyname=${onlyname/'_'/'-'}
    echo $onlyname

    # create copies of master deployment
    tempfilename='master-deployment-_.yaml'
    newname=${tempfilename/'_'/$onlyname}
    cp ./master-deployment.yaml $newname
    # echo $onlyname
    master="-master"
    slave="-slave"
    onlynamemaster="$onlyname$master"
    onlynameslave="$onlyname$slave"
    oldname='service_name'
    sed -i '' "s/${oldname}/${onlynamemaster}/g" $newname


    # create copies of slave deployment
    tempfilename='slave-deployment-_.yaml'
    newnameslave=${tempfilename/'_'/$onlyname}
    cp ./slave-deployment.yaml $newnameslave
    oldname='service_name'
    sed -i '' "s/${oldname}/${onlynameslave}/g" $newnameslave
    
    oldname='LOCUST_SERVICE_HOST'
    hostAppend="_service_host"
    newHost="$onlynamemaster$hostAppend"
    newHost=${newHost/'-'/'_'}
    newHost=${newHost/'-'/'_'}
    newHost=${newHost/'-'/'_'}
    newHost=`echo "${newHost}" | tr '[a-z]' '[A-Z]'`
    sed -i '' "s/${oldname}/${newHost}/g" $newnameslave
    
    oc process -f $newname | oc create -f -
    oc process -f $newnameslave | oc create -f -
    sh ./seed.sh $filename $temphost $onlynamemaster $onlynameslave

    # cleanup
    rm $newname $newnameslave
done