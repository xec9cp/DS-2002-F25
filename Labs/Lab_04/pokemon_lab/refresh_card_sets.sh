#!/bin/bash
set -e

RAW_DATA_DIR="card_set_lookup"

echo "Start refreshing all card sets in $RAW_DATA_DIR/..."

for json_file in "$RAW_DATA_DIR"/*.json; do
    SET_ID=$(basename "$json_file" .json)
    echo "Start updating the card set with set ID: $SET_ID ..."
    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}" -o "$json_file"
    echo "Card data saved to $json_file"
done

echo "All card sets done refreshing."