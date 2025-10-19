import os
import sys
import json
import pandas as pd


def _load_lookup_data(lookup_dir):
    all_lookup_df = []
    for filename in os.listdir(lookup_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(lookup_dir, filename)

            with open(filepath, "r") as file_pointer:
                data = json.load(file_pointer)

            df = pd.json_normalize(data["data"])

            df["card_market_value"] = (
                df.get("tcgplayer.prices.holofoil.market", pd.Series([None] * len(df)))
                .fillna(df.get("tcgplayer.prices.normal.market", pd.Series([None] * len(df))))
                .fillna(0.0)
            )

            df = df.rename(
                columns={
                    "id": "card_id",
                    "name": "card_name",
                    "number": "card_number",
                    "set.id": "set_id",
                    "set.name": "set_name",
                    "tcgplayer.prices...market": "card_market_value"
                }
            )

            required_cols = [
                "card_id",
                "card_name",
                "set_id",
                "set_name",
                "card_market_value"
            ]
            all_lookup_df.append(df[required_cols].copy())

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    lookup_df = (
        lookup_df.sort_values(by="card_market_value", ascending=False)
                 .drop_duplicates(subset=["card_id"], keep="first")
                 .reset_index(drop=True)
    )

    return lookup_df 

def _load_inventory_data(inventory_dir): 
    inventory_data = []
    for filename in os.listdir(inventory_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(inventory_dir, filename)
            df = pd.read_csv(filepath)
            inventory_data.append(df)
        if not inventory_data:
            return pd.DataFrame()
        inventory_df = pd.concat(inventory_data, ignore_index=True)
        inventory_df['card_id'] = (inventory_df['set_id'].astype("str").str.strip() + 
                                    '-' + 
                                    inventory_df['card_number'].astype("str").str.strip()) 
        return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    
    if inventory_df.empty:
        print("Error: inventory_df is empty.",  file=sys.stderr) 
        final_cols = [
            "index", "binder_name", "page_number", "slot_number",
            "card_id", "card_name", "set_name", "card_market_value"
        ]
        empty_df = pd.DataFrame(columns=final_cols)
        empty_df.to_csv(output_file, index=False)
        return

    merged_df = pd.merge(
        inventory_df,
        lookup_df[["card_id", "card_name", "set_name", "card_market_value"]],
        on="card_id",
        how="left"
    )
    
    if 'card_name_y' in merged_df.columns:
        merged_df['card_name'] = merged_df['card_name_y']
        merged_df = merged_df.drop(columns=['card_name_x', 'card_name_y'], errors='ignore')
    elif 'card_name_x' in merged_df.columns:
        merged_df = merged_df.rename(columns={'card_name_x': 'card_name'})

    merged_df['card_market_value'].fillna(0.0)
    merged_df['set_name'].fillna('NOT_FOUND')
    merged_df['index']=(merged_df['binder_name'].astype("str").str.strip() + "_" +
                        merged_df['page_number'].astype("str").str.strip() + "_" +
                        merged_df['slot_number'].astype("str").str.strip())
    
    final_cols = [
            "index", "binder_name", "page_number", "slot_number",
            "card_id", "card_name", "set_name", "card_market_value"
        ]

    merged_df.to_csv(output_file, columns=final_cols, index=False)
    print("Portfolio data has successfully been updated and saved as output_file. ")

def main():
    inventory_dir = "./card_inventory/"
    lookup_dir = "./card_set_lookup/"
    output_file = "card_portfolio.csv"
    update_portfolio(inventory_dir, lookup_dir, output_file)

def test():
    inventory_dir = "./card_inventory_test/"
    lookup_dir = "./card_set_lookup_test/"
    output_file = "test_card_portfolio.csv"
    update_portfolio(inventory_dir, lookup_dir, output_file)

if __name__ == "__main__":
    print("Test Mode On. Testing pokemon ETL script",  file=sys.stderr)
    test()



