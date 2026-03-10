import re

def extract_entities_from_text(text: str) -> dict:
    entities = {}

    customer_match = re.search(r"Claimant\s+([A-Za-z\s]+?)\s+was treated", text)
    provider_match = re.search(r"treated by\s+([A-Za-z\s]+?)\s+at", text)
    hospital_match = re.search(r"at\s+(H\d+)", text)
    device_match = re.search(r"device\s+(D\d+)", text)

    if customer_match:
        entities["customer_name"] = customer_match.group(1).strip()
    if provider_match:
        entities["provider_name"] = provider_match.group(1).strip()
    if hospital_match:
        entities["hospital_id"] = hospital_match.group(1).strip()
    if device_match:
        entities["device_id"] = device_match.group(1).strip()

    return entities


if __name__ == "__main__":
    sample = "Claimant John Smith was treated by Dr Patel at H301. Submitted from device D401."
    print(extract_entities_from_text(sample))