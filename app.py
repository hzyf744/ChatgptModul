import openai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = API_KEY


def get_input(prompt_message, is_keyword=False):
    """ 
    Genel giriş alma fonksiyonu.
    """
    while True:
        value = input(prompt_message).strip()
        if not value:
            print("This field cannot be left empty. Please provide a valid input.")
        else:
            if is_keyword:
                return ', '.join([keyword.strip() for keyword in value.split(',')])
            return value


def remove_repeated_sentences(text):
    """
    Tekrarlanan cümleleri metinden kaldır.
    """
    sentences = text.split("\n")
    seen = set()
    unique_sentences = [sentence for sentence in sentences if sentence not in seen and not seen.add(sentence)]
    return "\n".join(unique_sentences)


def generate_product_description(details):
    prompt = f"""
    Product: {details['product']}
    Category: {details['category']}
    Keywords: {details['keywords']}
    Product Features: {details['product_features']}
    Free Shipping: {details['free_shipping']}
    Personalizable: {details['personalizable']}
    Customizable: {details['customizable']}
    Return: Fast and free shipping, 30-day return warranty

    Based on the details provided, craft a compelling product description:

    1. Title (Short and attractive): 
    2. Product Promise (Why is this product unique?): 
    3. Problem & Solution (What problem does it solve?): 
    4. Description (Narrative style): 
    5. Benefits & Features: 
    - Example: Long-lasting battery
    - ...
    6. Why Choose Us (Highlight one main feature): 
    7. Usage Areas (Where or when can this product be used?): 
    8. CTA: (Note: Avoid using the verb "Enjoy". Use other compelling verbs like "Discover", "Experience")
    9. Services (Any additional services?): 
   10. Shop Introduction (Tell a short story about the shop):

🔍 Ensure that:
- The title is catchy.
- Product promise is clear.
- Keywords are incorporated naturally.
"""

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.1,
            max_tokens=600
        )
        description = response.choices[0].text.strip()
        description = remove_repeated_sentences(description)
        return description
    except Exception as e:
        return f"An issue occurred with the OpenAI API: {str(e)}"


if __name__ == "__main__":
    details = {
        'product': get_input("Please enter your product: "),
        'category': get_input("Please enter the category: "),
        'keywords': get_input("Please enter the keywords separated by commas: ", is_keyword=True),
        'product_features':input("Please enter the product features separated by commas (leave empty if none): "),
        'free_shipping': get_input("Is there free shipping? (yes/no): "),
        'personalizable': get_input("Is the product personalizable? (yes/no): "),
        'customizable': get_input("Is the product customizable? (yes/no): "),
        'return': get_input("Is the product returnable? (yes/no): ")
    }

    description = generate_product_description(details)
    print("\nGenerated Product Description:")
    print(description)
