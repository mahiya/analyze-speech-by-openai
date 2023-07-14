export OPENAI_NAME=$(cat settings.json | jq '.OPENAI_NAME' | sed "s/\"//g")
export OPENAI_KEY=$(cat settings.json | jq '.OPENAI_KEY' | sed "s/\"//g")
export OPENAI_MODEL=$(cat settings.json | jq '.OPENAI_MODEL' | sed "s/\"//g")
export OPENAI_API_VERSION=$(cat settings.json | jq '.OPENAI_API_VERSION' | sed "s/\"//g")
export OPENAI_SYSTEM_MESSAGE=$(cat settings.json | jq '.OPENAI_SYSTEM_MESSAGE' | sed "s/\"//g")
export OPENAI_MAX_TOKEN=$(cat settings.json | jq '.OPENAI_MAX_TOKEN' | sed "s/\"//g")
export OPENAI_TEMPERATURE=$(cat settings.json | jq '.OPENAI_TEMPERATURE' | sed "s/\"//g")
export SPEECH_SERVICE_REGION=$(cat settings.json | jq '.SPEECH_SERVICE_REGION' | sed "s/\"//g")
export SPEECH_SERVICE_KEY=$(cat settings.json | jq '.SPEECH_SERVICE_KEY' | sed "s/\"//g")

python app.py