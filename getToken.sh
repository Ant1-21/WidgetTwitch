#!/bin/bash

############################################################
# Help                                                     #
############################################################
function usage()
{
    # Display Help
    echo ""
    echo "Get Twitch application Token"
    echo ""
    echo "Usage: $0 --id string --secret string"
    echo "" 
    echo "options:"
    echo "--id      Set user id."
    echo "--secret  Set user secret."
    echo "--help    Print this Help."
    echo ""
}

# This is a while loop that is checking if the number of arguments is greater than 0. If it is, it
# will check if the first argument is --help. If it is, it will print help and exit. If it is not, it
# will check if the first argument starts with --. If it does, it will set the variable v to the first
# argument without the -- and set the variable to the second argument. It will then shift the
# arguments. It will then shift the arguments again.
while [ $# -gt 0 ]; do
    if [[ $1 == "--help" ]]; then
        echo "Help"
        usage
        exit 0
    elif [[ $1 == "--"* ]]; then
        v="${1/--/}"
        declare "$v"="$2"
        shift
    fi
    shift
done

# This is checking if the id and secret are empty. If they are, it will print the usage and exit.
if [[ -z $id ]]; then
    usage
    echo "Script failed: Missing parameter --id"
    exit 1
elif [[ -z $secret ]]; then
    usage
    echo "Script failed: Missing parameter --secret"
    exit 1
fi

# This is a curl command that is sending a POST request to the url https://id.twitch.tv/oauth2/token.
curl -X POST 'https://id.twitch.tv/oauth2/token' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d "client_id=${id}&client_secret=${secret}&grant_type=client_credentials"
