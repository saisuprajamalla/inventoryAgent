from inventory_agent import InventoryAgent

# Initialize the InventoryAgent
agent = InventoryAgent(role="Inventory Manager", goal="Generate attributes", backstory="Testing prompts", api_key="your_huggingface_api_key")

# List of business types to test
business_types = [
    "retail", "grocery", "electronics", "pharmacy", "furniture",
    "clothing", "automotive", "hospitality", "food service",
    "beauty products", "hardware", "books", "sports equipment",
    "toys", "medical supplies"
]

# Comments and attributes to simulate the test
comments = "Generate inventory setup for this business type."
sku_count = 3
attributes = ["Quantity", "Expiration Date", "Location"]

# Iterate over business types and generate inventory templates
results = []
for business_type in business_types:
    print(f"Testing business type: {business_type}")
    try:
        response = agent.generate_inventory_template(business_type, sku_count, attributes, comments)
        results.append({"business_type": business_type, "response": response})
        print(f"Results for {business_type}: {response}")
    except Exception as e:
        print(f"Error testing {business_type}: {e}")

# Optional: Save results to a file for review
import json
with open("test_results.json", "w") as file:
    json.dump(results, file, indent=4)