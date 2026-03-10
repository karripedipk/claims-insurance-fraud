import pandas as pd
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

feature_query = """
MATCH (cl:Claim)
OPTIONAL MATCH (cl)-[:SUBMITTED_FROM]->(d:Device)<-[:SUBMITTED_FROM]-(other_claim:Claim)
OPTIONAL MATCH (cl)-[:TREATED_BY]->(p:Provider)<-[:TREATED_BY]-(provider_claim:Claim)
OPTIONAL MATCH (cl)-[:PAID_TO]->(b:BankAccount)<-[:PAID_TO]-(bank_claim:Claim)
RETURN
    cl.claim_id AS claim_id,
    cl.claim_amount AS claim_amount,
    COUNT(DISTINCT other_claim) - 1 AS shared_device_claim_count,
    COUNT(DISTINCT provider_claim) - 1 AS same_provider_claim_count,
    COUNT(DISTINCT bank_claim) - 1 AS same_bank_claim_count
"""

def fetch_features():
    with driver.session() as session:
        result = session.run(feature_query)
        rows = [record.data() for record in result]
        return pd.DataFrame(rows)

if __name__ == "__main__":
    df = fetch_features()
    print(df)
    df.to_csv("data/claim_features.csv", index=False)
    driver.close()