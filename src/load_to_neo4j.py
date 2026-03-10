import pandas as pd
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "password"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def run_query(query, params=None):
    with driver.session() as session:
        session.run(query, params or {})

def create_constraints():
    queries = [
        "CREATE CONSTRAINT customer_id IF NOT EXISTS FOR (c:Customer) REQUIRE c.customer_id IS UNIQUE",
        "CREATE CONSTRAINT claim_id IF NOT EXISTS FOR (c:Claim) REQUIRE c.claim_id IS UNIQUE",
        "CREATE CONSTRAINT provider_id IF NOT EXISTS FOR (p:Provider) REQUIRE p.provider_id IS UNIQUE",
        "CREATE CONSTRAINT device_id IF NOT EXISTS FOR (d:Device) REQUIRE d.device_id IS UNIQUE",
        "CREATE CONSTRAINT bank_id IF NOT EXISTS FOR (b:BankAccount) REQUIRE b.bank_account_id IS UNIQUE",
        "CREATE CONSTRAINT policy_id IF NOT EXISTS FOR (p:Policy) REQUIRE p.policy_id IS UNIQUE"
    ]
    for q in queries:
        run_query(q)

def load_customers(customers_df):
    query = """
    MERGE (c:Customer {customer_id: $customer_id})
    SET c.name = $name,
        c.dob = $dob,
        c.address = $address,
        c.phone = $phone,
        c.email = $email
    """
    for _, row in customers_df.iterrows():
        run_query(query, row.to_dict())

def load_providers(providers_df):
    query = """
    MERGE (p:Provider {provider_id: $provider_id})
    SET p.provider_name = $provider_name,
        p.specialty = $specialty
    """
    for _, row in providers_df.iterrows():
        run_query(query, row.to_dict())

def load_claims(claims_df):
    query = """
    MERGE (cl:Claim {claim_id: $claim_id})
    SET cl.claim_amount = toFloat($claim_amount),
        cl.claim_type = $claim_type,
        cl.status = $status

    MERGE (cu:Customer {customer_id: $customer_id})
    MERGE (po:Policy {policy_id: $policy_id})
    MERGE (pr:Provider {provider_id: $provider_id})
    MERGE (dv:Device {device_id: $device_id})
    MERGE (ba:BankAccount {bank_account_id: $bank_account_id})
    MERGE (ho:Hospital {hospital_id: $hospital_id})

    MERGE (cu)-[:FILED]->(cl)
    MERGE (cl)-[:UNDER_POLICY]->(po)
    MERGE (cl)-[:TREATED_BY]->(pr)
    MERGE (pr)-[:AFFILIATED_WITH]->(ho)
    MERGE (cl)-[:SUBMITTED_FROM]->(dv)
    MERGE (cl)-[:PAID_TO]->(ba)
    """
    for _, row in claims_df.iterrows():
        run_query(query, row.to_dict())

if __name__ == "__main__":
    customers_df = pd.read_csv("data/customers.csv")
    providers_df = pd.read_csv("data/providers.csv")
    claims_df = pd.read_csv("data/claims.csv")

    create_constraints()
    load_customers(customers_df)
    load_providers(providers_df)
    load_claims(claims_df)

    driver.close()
    print("Loaded data into Neo4j.")