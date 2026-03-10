import pandas as pd
from difflib import SequenceMatcher

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def resolve_customers(customers_df: pd.DataFrame, threshold: float = 0.85):
    resolved = []
    visited = set()

    for i, row_i in customers_df.iterrows():
        if i in visited:
            continue

        group = [row_i["customer_id"]]
        visited.add(i)

        for j, row_j in customers_df.iterrows():
            if j in visited or i == j:
                continue

            name_score = similarity(row_i["name"], row_j["name"])
            dob_match = row_i["dob"] == row_j["dob"]
            phone_match = row_i["phone"] == row_j["phone"]

            if name_score >= threshold and dob_match and phone_match:
                group.append(row_j["customer_id"])
                visited.add(j)

        resolved.append({
            "canonical_customer_id": row_i["customer_id"],
            "merged_ids": group
        })

    return pd.DataFrame(resolved)

if __name__ == "__main__":
    customers = pd.read_csv("data/customers.csv")
    result = resolve_customers(customers)
    print(result)