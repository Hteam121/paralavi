import openai
import pandas as pd
import random
from tqdm import tqdm  

#took out the key for git purpose
openai.api_key = ""

# Define product categories and stores
categories = ["produce", "dairy", "bakery", "meat", "grocery"]
stores = ["Costco", "Kroger", "Walmart"]
product_types = ["apple", "milk", "bread", "chicken", "coffee", "rice", "eggs", "pasta", "lettuce", "tomatoes"]

# Function to generate product details using OpenAI ChatCompletion
def generate_product_details(product_type, store, category):
    prompt = f"Generate a detailed product description, brand name, and realistic price for {product_type} in the {category} category sold at {store}."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        # Extract the generated content
        description = response['choices'][0]['message']['content'].strip()
        
        brand = f"{store} {product_type.capitalize()} Brand"
        price = round(random.uniform(1, 20), 2)  
        
        return {
            "item_name": product_type,
            "category": category,
            "store": store,
            "brand": brand,
            "price": price,
            "description": description
        }
    
    except Exception as e:
        print(f"Error generating data for {product_type} in {store}: {e}")
        return None

product_data = []
total_items = len(stores) * len(product_types) * 50 

with tqdm(total=total_items, desc="Generating Products") as pbar:
    for store in stores:
        for product_type in product_types:
            for i in range(50):  
                category = random.choice(categories)
                product_details = generate_product_details(product_type, store, category)
                if product_details:
                    product_data.append(product_details)
                    
                pbar.update(1)
                if i % 500 == 0:
                    print(f"Generated {i + 1} items for {product_type} in {store}")

# save as CSV
product_df = pd.DataFrame(product_data)
product_df.to_csv("realistic_products.csv", index=False)

print("Data generation complete! Saved to realistic_products.csv.")

