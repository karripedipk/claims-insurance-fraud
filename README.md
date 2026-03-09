# Ontology for this project
## Node labels
	•	Customer
	•	Claim
	•	Policy
	•	Provider
	•	Hospital
	•	Device
	•	Vehicle
	•	BankAccount
	•	Address
	•	Document
## Relationships
	•	(:Customer)-[:FILED]->(:Claim)
	•	(:Claim)-[:UNDER_POLICY]->(:Policy)
	•	(:Claim)-[:TREATED_BY]->(:Provider)
	•	(:Provider)-[:AFFILIATED_WITH]->(:Hospital)
	•	(:Claim)-[:SUBMITTED_FROM]->(:Device)
	•	(:Claim)-[:PAID_TO]->(:BankAccount)
	•	(:Customer)-[:LIVES_AT]->(:Address)
	•	(:Customer)-[:OWNS]->(:Vehicle)
	•	(:Document)-[:DESCRIBES]->(:Claim)

# Step 1: Entity extraction from documents

# Step 2: Entity resolution

# Step 3: Load graph into Neo4j

# Step 4: Fraud investigation queries in Neo4j

# Step 5: Generate ML features from graph signals

# Step 6: Train anomaly detection model

# Step 7: Graph-derived risk score