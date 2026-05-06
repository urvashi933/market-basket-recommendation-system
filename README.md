# Market Basket Recommendation System

## Project Title
Market Basket Analysis and Product Recommendation System

## Business Problem
The retail company aims to improve product placement, cross-selling, upselling, and promotional bundling by understanding customer purchasing behavior. By identifying which products are frequently bought together, the business can make better product recommendations, design effective bundle offers, and optimize store layouts, leading to increased sales and enhanced customer experience.

## Dataset Description
The dataset contains transaction records from a retail store. The key columns include:
- `TransactionID`: A unique identifier for each transaction/invoice.
- `CustomerID`: A unique identifier for the customer making the purchase.
- `TransactionDate`: The date of the transaction.
- `ProductID`: A unique identifier for the product purchased.
- `ProductName`: The name/description of the product.
- `Quantity`: The number of units of the product purchased in the transaction.
- `UnitPrice`: The price of a single unit of the product.

**Data Understanding:**
- **Transaction:** Represents a single purchase event made by a customer at a specific time, identified by a unique `TransactionID`.
- **Item:** Represents a unique product purchased during the transaction, identified by `ProductID` and `ProductName`.
- **Row:** Represents a single item purchased within a specific transaction. A transaction with multiple items will have multiple rows.
- **Why Market Basket Analysis is useful:** It helps uncover hidden associations between products, revealing purchasing patterns. This knowledge is crucial for inventory management, targeted marketing, and store layout optimization.
- **Cross-selling & Upselling:** Associations like "customers who buy A also buy B" can be used to recommend product B to a customer buying A (cross-selling). It can also help in bundling a low-selling item with a high-selling item to clear stock.

## Data Cleaning Summary
The following cleaning steps were performed to ensure data quality:
1. **Invalid Quantities:** Removed rows with `Quantity` <= 0 (e.g., cancelled or returned items).
2. **Missing Product Names:** Removed rows where `ProductName` was missing/NaN, as they cannot be used for product recommendations.
3. **Data Types:** Converted `TransactionDate` to datetime format.
4. **Duplicates:** Dropped duplicate records for the same `TransactionID` and `ProductName` to avoid inflating the frequency of items within a single transaction.

## Basket Preparation Method
The raw transactional data was converted into a pivot table (basket format) where each row represents a unique `TransactionID` and each column represents a unique `ProductName`. 
- The cell values initially contained the sum of `Quantity` for each item in a transaction.
- We then applied an encoding function: if the quantity was >= 1, it was converted to `1` (indicating the product was purchased). If the value was 0 or less, it remained `0` (not purchased). This binary format is required by association rule algorithms.

## Frequent Itemsets Summary
Frequent itemsets were generated using the **FP-Growth algorithm**. We tested multiple minimum support values (e.g., 0.01, 0.05, 0.1) and plotted the number of generated itemsets.
- We chose a minimum support of **0.05 (5%)** because it provided a reasonable balance: it filtered out extremely rare combinations that aren't useful for general business strategies while retaining enough significant patterns to generate meaningful rules.

## Association Rules Summary
Association rules were generated using the following metrics:
- **Support:** The fraction of total transactions that contain both the antecedent and consequent. It tells us how popular an itemset is.
- **Confidence:** The conditional probability that a customer will buy the consequent given they bought the antecedent. It tells us how reliable the rule is.
- **Lift:** The ratio of the observed support to the expected support if the items were independent. A lift > 1 indicates a positive association (they are bought together more often than expected by chance). It measures the strength of the association.

We filtered the rules to retain those with `lift > 1.2` and `confidence > 0.3`.

## Top Rules with Interpretation
Here are some of the top meaningful association rules discovered:

1. **Rule:** `Dishwash Liquid` $\rightarrow$ `Fabric Softener`
   - **Support:** 5.23% | **Confidence:** 71.76% | **Lift:** 8.55
   - **Interpretation:** Customers buying Dishwash Liquid are 8.55 times more likely to buy Fabric Softener than if the two were unrelated. 71.76% of Dishwash Liquid buyers also buy Fabric Softener.
   - **Business Meaning:** Strong association between cleaning supplies.

2. **Rule:** `Nachos` $\rightarrow$ `Salsa Dip`
   - **Support:** 5.78% | **Confidence:** 77.04% | **Lift:** 7.92
   - **Interpretation:** 77.04% of customers who buy Nachos also buy Salsa Dip.
   - **Business Meaning:** Classic snack combination. Highly predictable pairing.

3. **Rule:** `Potato Chips` $\rightarrow$ `Salsa Dip`
   - **Support:** 5.45% | **Confidence:** 73.13% | **Lift:** 7.52
   - **Interpretation:** Similar to Nachos, Potato Chips buyers frequently add Salsa Dip to their basket.

4. **Rule:** `Butter`, `Bread Loaf` $\rightarrow$ `Chocolate Spread`
   - **Support:** 5.11% | **Confidence:** 86.79% | **Lift:** 7.23
   - **Interpretation:** An overwhelming 86.79% of customers buying both Butter and Bread Loaf also purchase Chocolate Spread.
   - **Business Meaning:** Strong breakfast routine combination.

5. **Rule:** `Butter` $\rightarrow$ `Chocolate Spread`
   - **Support:** 8.12% | **Confidence:** 82.49% | **Lift:** 6.87
   - **Interpretation:** Customers who buy Butter alone also have a very high likelihood (82.49%) of buying Chocolate Spread.
   - **Business Meaning:** Strong standalone breakfast spread association.

6. **Rule:** `Chocolate Spread` $\rightarrow$ `Butter`
   - **Support:** 8.12% | **Confidence:** 67.59% | **Lift:** 6.87
   - **Interpretation:** Conversely, 67.59% of Chocolate Spread buyers also purchase Butter.
   - **Business Meaning:** Demonstrates a bidirectional relationship; both products drive the sale of the other.

7. **Rule:** `Bread Loaf` $\rightarrow$ `Chocolate Spread`
   - **Support:** 7.78% | **Confidence:** 82.35% | **Lift:** 6.86
   - **Interpretation:** 82.35% of Bread Loaf purchasers add Chocolate Spread to their transaction.
   - **Business Meaning:** Bread acts as an excellent "anchor" product to drive sales of sweet spreads.

8. **Rule:** `Chocolate Spread` $\rightarrow$ `Bread Loaf`
   - **Support:** 7.78% | **Confidence:** 64.81% | **Lift:** 6.86
   - **Interpretation:** About 65% of people buying Chocolate Spread are also buying Bread Loaf.
   - **Business Meaning:** Highlights that while bread drives spread sales heavily, the reverse is also decently strong.

9. **Rule:** `Chocolate Spread`, `Bread Loaf` $\rightarrow$ `Butter`
   - **Support:** 5.11% | **Confidence:** 65.71% | **Lift:** 6.68
   - **Interpretation:** If a customer already has Chocolate Spread and Bread Loaf in their basket, there is a 65.71% chance they will also buy Butter.
   - **Business Meaning:** Confirms the viability of a 3-item breakfast bundle.

10. **Rule:** `Chocolate Spread`, `Butter` $\rightarrow$ `Bread Loaf`
   - **Support:** 5.11% | **Confidence:** 63.01% | **Lift:** 6.67
   - **Interpretation:** Customers buying both spreads (Chocolate and Butter) will buy Bread Loaf 63% of the time.
   - **Business Meaning:** These three items are strongly interconnected, regardless of which two the customer starts with.

## Final Business Recommendations
1. **Product Bundling:** 
   - Create a "Breakfast Bundle" containing Bread Loaf, Butter, and Chocolate Spread.
   - Create a "Cleaning Essentials Kit" containing Dishwash Liquid and Fabric Softener.
2. **Store Layout (Placement):**
   - Place Salsa Dip directly adjacent to the Nachos and Potato Chips aisles to capture impulse buyers.
   - Position Chocolate Spread near the bread and bakery section.
3. **Cross-Selling:**
   - In the online store, if a user adds Nachos to their cart, immediately trigger a pop-up recommendation: "Pairs perfectly with Salsa Dip!"
   - If a customer buys Dishwash Liquid, offer a small discount on Fabric Softener at checkout.
4. **Promotional Campaigns:**
   - Run a weekend promotion: "Buy Nachos, get 20% off Salsa Dip." This capitalizes on the high confidence rule to drive total basket value.
5. **Rules to Ignore:**
   - Rules with high support but lift close to 1 should be ignored. For example, if "Bread Loaf $\rightarrow$ Milk" has a lift of 1.0, it just means both are very popular items bought frequently, but one does not drive the purchase of the other. Promotions should focus on rules with high lift.

## How to run the project
1. Clone this repository.
2. Ensure you have Python 3.8+ installed.
3. Install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the main script to generate outputs and visualizations:
   ```bash
   python main.py
   ```
5. Check the `outputs/` folder for CSVs containing frequent itemsets and association rules.
6. Check the `images/` folder for generated plots.
