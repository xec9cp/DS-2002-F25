#!/bin/bash

set -e

RAW_DATA_DIR="card_set_lookup"

echo "Start refreshing all card sets in card_set_lookup/..."

for json_file in "$RAW_DATA_DIR/"/*.json; do
    SET_ID=$(basename "$FILE" .json)
    echo "Start updating the card set with set ID: $SET_ID ..."
    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$FILE"
    echo "Card data saved to $FILE"
done

echo "All card sets done refreshing."