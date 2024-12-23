from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import re

class InventoryAgent:
    def __init__(self, role, goal, backstory, api_key=None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.api_key = api_key

        # Initialize Hugging Face model and tokenizer
        model_name = "bigscience/bloom-560m"  # Adjust model as needed
        self.generator = pipeline(
            "text-generation",
            model=AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=api_key),
            tokenizer=AutoTokenizer.from_pretrained(model_name),
        )

    # def generate_inventory_prompt(self, businessType, comments):
    #     if businessType.lower() == "retail":
    #         prompt = (
    #             f"List inventory attributes for a Retail business. Use 1-2 words per attribute and separate by commas.\n"
    #             f"Examples: SKU, Category, Price, Quantity, Restocking Frequency, Storage Location.\n"
    #             f"Context: {comments}\n"
    #             f"Output: A comma-separated list of attributes."
    #         )
    #     elif businessType.lower() == "grocery":
    #         prompt = (
    #             f"List inventory attributes for a Grocery business. Use 1-2 words per attribute and separate by commas.\n"
    #             f"Examples: SKU, Category, Organic, Freshness, Storage Temperature, Expiration Date.\n"
    #             f"Context: {comments}\n"
    #             f"Output: A comma-separated list of attributes."
    #         )
    #     else:
    #         prompt = (
    #             f"List inventory attributes for a {businessType.capitalize()} business. Use 1-2 words per attribute and separate by commas.\n"
    #             f"Context: {comments}\n"
    #             f"Output: A comma-separated list of attributes."
    #         )
    #     return prompt

    def generate_inventory_prompt(self, businessType, comments):
        if businessType.lower() == "retail":
            prompt = (
                f"Generate unique and concise inventory attributes for a Retail business as a comma-separated list.\n"
                f"Examples: SKU, Category, Price, Quantity, Restocking Frequency, Storage Location.\n"
                f"Ensure the attributes are relevant to retail inventory management and do not repeat examples unnecessarily.\n"
                f"Context: {comments}\n"
                f"Output: A comma-separated list of attributes."
            )
        elif businessType.lower() == "food & beverage":
            prompt = (
                f"Generate unique and concise inventory attributes for a Food & Beverage business as a comma-separated list.\n"
                f"Examples: SKU, Category, Freshness, Storage Temperature, Expiration Date, Packaging Type.\n"
                f"Ensure the attributes are relevant to food inventory management and avoid irrelevant or redundant entries.\n"
                f"Context: {comments}\n"
                f"Output: A comma-separated list of attributes."
            )
        elif businessType.lower() == "electronics":
            prompt = (
                f"Generate unique and concise inventory attributes for an Electronics business as a comma-separated list.\n"
                f"Examples: SKU, Model Number, Warranty Period, Power Rating, Quantity, Manufacturer.\n"
                f"Ensure the attributes are specific to electronics inventory and relevant to the context.\n"
                f"Context: {comments}\n"
                f"Output: A comma-separated list of attributes."
            )
        else:
            prompt = (
                f"Generate unique and concise inventory attributes for a {businessType.capitalize()} business as a comma-separated list.\n"
                f"Include attributes relevant to inventory management and avoid redundancy.\n"
                f"Context: {comments}\n"
                f"Output: A comma-separated list of attributes."
            )
        return prompt

    def clean_generated_text(self, text):
        """
        Extract and clean the attributes from the LLM response.
        """
        attributes = text.split("Output:")[-1].strip()  # Extract content after "Output:"
        attributes = re.split(r",|\n", attributes)  # Split by commas or new lines
        attributes = [attr.strip() for attr in attributes if attr.strip()]  # Remove empty entries
        attributes = [re.sub(r'[^a-zA-Z0-9\s]', '', attr) for attr in attributes]  # Remove special characters
        attributes = [attr for attr in attributes if
                      not attr.lower().startswith("a commaseparated")]  # Remove verbose phrases
        return list(dict.fromkeys(attributes))  # Remove duplicates

    def generate_mock_data(self, attribute, businessType):
        """
        Generate deterministic mock data for standard attributes or provide fallback for unknown attributes.
        """
        predefined_mock_data = {
            "SKU": lambda: f"SKU-{businessType[:3].upper()}",
            "Category": lambda: businessType.capitalize(),
            "Quantity": lambda: "100",
            "Price": lambda: "$10.99",
            "Expiration Date": lambda: "2024-12-31",
            "Location": lambda: "Warehouse A",
            "Freshness": lambda: "High",
            "Organic": lambda: "Yes",
            "Restocking Frequency": lambda: "Monthly",
            "Model Number": lambda: f"Model-{businessType[:3].upper()}-123",
        }
        if attribute in predefined_mock_data:
            return predefined_mock_data[attribute]()
        else:
            # Fallback for unknown attributes
            return f"Mock-{attribute.replace(' ', '-').capitalize()}"

    def validate_attributes(self, attributes):
        """
        Validate and refine the list of attributes to ensure relevance and uniqueness.
        """
        valid_attributes = []
        seen = set()
        for attr in attributes:
            attr = attr.lower().strip()
            if attr and attr not in seen and len(attr) > 2:  # Ignore single-character or very short attributes
                valid_attributes.append(attr.title())  # Title-case for consistency
                seen.add(attr)
        return valid_attributes

    def generate_inventory_template(self, businessType, skuCount, attributes, comments):
        """
        Generate a complete inventory template for the given business type.
        """
        # Generate attributes
        prompt = self.generate_inventory_prompt(businessType, comments)
        try:
            llm_response = self.generator(prompt, max_new_tokens=50, num_return_sequences=1)
            generated_text = llm_response[0]["generated_text"]
            generated_attributes = self.clean_generated_text(generated_text)
        except Exception as e:
            # Fallback on error
            generated_attributes = []

        # Validate attributes
        validated_attributes = self.validate_attributes(generated_attributes)

        # Fallback for empty or invalid attributes
        if not validated_attributes:
            validated_attributes = ["SKU", "Category", "Price", "Quantity"]

        # Combine headers without duplicates
        seen_headers = set()
        headers = []
        for header in ["SKU Name", "Category"] + attributes + validated_attributes:
            if header not in seen_headers:
                headers.append(header)
                seen_headers.add(header)

        # Generate rows with mock data
        rows = []
        for i in range(1, skuCount + 1):
            row = [f"SKU-{i}", businessType]
            row += [self.generate_mock_data(attr, businessType) for attr in headers[2:]]
            rows.append(row)

        return {"headers": headers, "rows": rows}