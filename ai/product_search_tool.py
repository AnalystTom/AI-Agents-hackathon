from crewai_tools import BaseTool
import pandas as pd
import json
from typing import Any
from pydantic import ConfigDict

class ProductSearchTool(BaseTool):
    name: str = "Product Search Tool"
    description: str = "Searches for products based on customer preferences."
    product_data: pd.DataFrame

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _run(self, text: str) -> str:
        customer_needs = json.loads(text)
        filtered_products = self.product_data.copy()

        # Apply filters based on customer needs
        if 'category' in customer_needs:
            filtered_products = filtered_products[
                filtered_products['category'].str.contains(customer_needs['category'], case=False, na=False)
            ]
        if 'brand' in customer_needs:
            filtered_products = filtered_products[
                filtered_products['brand'].str.contains(customer_needs['brand'], case=False, na=False)
            ]
        if 'price_range' in customer_needs:
            min_price, max_price = customer_needs['price_range']
            filtered_products = filtered_products[
                (filtered_products['price'] >= min_price) & (filtered_products['price'] <= max_price)
            ]
        if 'features' in customer_needs:
            features = customer_needs['features'].split(',')
            for feature in features:
                feature = feature.strip()
                filtered_products = filtered_products[
                    filtered_products['features'].str.contains(feature, case=False, na=False)
                    | filtered_products['Product Description'].str.contains(feature, case=False, na=False)
                    | filtered_products['Product Tags'].str.contains(feature, case=False, na=False)
                ]

        # Select top 2-3 products
        recommended_products = filtered_products.head(3)
        products_list = recommended_products.to_dict('records')
        return json.dumps(products_list)
