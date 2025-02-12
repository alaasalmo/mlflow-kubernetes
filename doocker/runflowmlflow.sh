#!/bin/bash

if [ ! -d /mlflow/469830549280038827 ]
then
    mkdir /mlflow/469830549280038827	
else
    echo "/mlflow/469830549280038827 already exists" 1>&2
fi

if [ ! -d /mlflow/mlflowdb ]
then
    mkdir /mlflow/mlflowdb	
else
    echo "/mlflow/mlflowdb already exists" 1>&2
fi

if [ ! -d /mlflow/mlruns ]
then
    mkdir /mlflow/mlruns	
else
    echo "/mlflow/mlruns already exists" 1>&2
fi

mlflow server --backend-store-uri=sqlite:////mlflow/mlflowdb/mlflow.db --default-artifact-root=file:///mlflow/mlruns --host 0.0.0.0 --port 5050
#tail -f /dev/null