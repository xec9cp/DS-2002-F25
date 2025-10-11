#!/bin/bash
set -e

echo "TCG Card Set ID"

read -r SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

URL="https://api.pokemontcg.io/v2/sets/$SET_ID"
OUTPUT_FILE="card_set_lookup/${SET_ID}.json"

echo "  -> Fetching data for $SET_ID..."

curl --request GET 
  --url https://api.pokemontcg.io/v2/sets/$SET_ID 
  --header 'X-Api-Key: <api_key_here>'

curl -s "$URL" -o "$OUTPUT_FILE" 2>&1
    
if [ $? -ne 0 ]; then
    echo "Error: curl failed for $SET_ID." >&2
    exit 1
fi
      
if [ ! -s "$OUTPUT_FILE" ] || [ "$(jq 'length' "$OUTPUT_FILE")" -eq 0 ]; then
    echo "Warning: No Card Set data found for $SET_ID. The API returned an empty response." >&2
else
    echo "  -> Data for $SET_ID saved successfully."
fi

echo "Data fetching complete. Check the 'card_set_lookup' directory."

