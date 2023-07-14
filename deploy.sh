#!/bin/bash -e
region='japaneast'
resourceGroup=$1 # デプロイ先のリソースグループ名を引数で取得する
sku='B1'
runtime='PYTHON:3.9'

export OPENAI_NAME=$(cat settings.json | jq '.OPENAI_NAME' | sed "s/\"//g")
export OPENAI_KEY=$(cat settings.json | jq '.OPENAI_KEY' | sed "s/\"//g")
export OPENAI_MODEL=$(cat settings.json | jq '.OPENAI_MODEL' | sed "s/\"//g")
export OPENAI_API_VERSION=$(cat settings.json | jq '.OPENAI_API_VERSION' | sed "s/\"//g")
export OPENAI_SYSTEM_MESSAGE=$(cat settings.json | jq '.OPENAI_SYSTEM_MESSAGE' | sed "s/\"//g")
export OPENAI_MAX_TOKEN=$(cat settings.json | jq '.OPENAI_MAX_TOKEN' | sed "s/\"//g")
export OPENAI_TEMPERATURE=$(cat settings.json | jq '.OPENAI_TEMPERATURE' | sed "s/\"//g")
export SPEECH_SERVICE_REGION=$(cat settings.json | jq '.SPEECH_SERVICE_REGION' | sed "s/\"//g")
export SPEECH_SERVICE_KEY=$(cat settings.json | jq '.SPEECH_SERVICE_KEY' | sed "s/\"//g")

az group create \
    --location $region \
    --resource-group $resourceGroup

name=($(az webapp up \
        --location $region \
        --resource-group $resourceGroup \
        --sku $sku \
        --runtime $runtime \
        --query 'name' \
        --output tsv))

az webapp config appsettings set \
    --resource-group $resourceGroup \
    --name $name \
    --settings "OPENAI_NAME=$OPENAI_NAME" \
               "OPENAI_KEY=$OPENAI_KEY" \
               "OPENAI_MODEL=$OPENAI_MODEL" \
               "OPENAI_API_VERSION=$OPENAI_API_VERSION" \
               "OPENAI_SYSTEM_MESSAGE=$OPENAI_SYSTEM_MESSAGE" \
               "OPENAI_MAX_TOKEN=$OPENAI_MAX_TOKEN" \
               "OPENAI_TEMPERATURE=$OPENAI_TEMPERATURE" \
               "SPEECH_SERVICE_REGION=$SPEECH_SERVICE_REGION" \
               "SPEECH_SERVICE_KEY=$SPEECH_SERVICE_KEY"