from flask import Flask, request, jsonify
from inventory_agent import InventoryAgent

HUGGING_FACE_API_KEY = "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"

# Initialize Flask App and Inventory Agent
app = Flask(__name__)
agent = InventoryAgent(
    role="An AI Agent specializing in inventory management.",
    goal="Assist users in setting up and managing inventory templates dynamically.",
    backstory="You are a highly experienced inventory management assistant trained to handle various business requirements.",
    api_key=HUGGING_FACE_API_KEY
)

print(agent)

@app.route("/generate-inventory-template", methods=["POST"])
def generate_inventory_template():
    try:
        # Get user input from the POST request
        data = request.json
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload."}), 400

        businessType = data.get("businessType", "General")
        skuCount = data.get("skuCount", 5)
        attributes = data.get("attributes", [])
        comments = data.get("comments", "")

        # Validate required fields
        if not businessType or not isinstance(skuCount, int):
            return jsonify({"error": "Invalid input. Ensure 'businessType' is provided and 'skuCount' is an integer."}), 400

        # Use the agent to generate the inventory template
        result = agent.generate_inventory_template(
            businessType=businessType,
            skuCount=skuCount,
            attributes=attributes,
            comments=comments
        )
        return jsonify(result)

    except Exception as e:
        # Log the exception and return an error response
        app.logger.error(f"Error generating inventory template: {e}")
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500

@app.before_request
def log_request_info():
    app.logger.info(f"Request Headers: {request.headers}")
    app.logger.info(f"Request Data: {request.get_json()}")


if __name__ == "__main__":
    app.run(debug=True)
