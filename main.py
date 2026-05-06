import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create outputs directory
os.makedirs('outputs', exist_ok=True)
os.makedirs('images', exist_ok=True)

# 1. Data Understanding & Loading
print("Loading dataset...")
df = pd.read_csv('dataset/part_2_market_basket_analysis.csv')

# 2. Data Cleaning
print("Cleaning data...")
# Cancelled transactions & invalid quantities (<=0)
df_clean = df[df['Quantity'] > 0]
# Missing product names
df_clean = df_clean.dropna(subset=['ProductName'])
# Incorrect data types (Ensure Date is datetime)
df_clean['TransactionDate'] = pd.to_datetime(df_clean['TransactionDate'])
# Duplicate transaction-product records
df_clean = df_clean.drop_duplicates(subset=['TransactionID', 'ProductName'])

# 3. Transaction Basket Preparation
print("Preparing basket...")
basket = (df_clean.groupby(['TransactionID', 'ProductName'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('TransactionID'))

# Convert quantities to 1 (purchased) and 0 (not purchased)
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)

# 4. Frequent Itemset Generation
print("Generating frequent itemsets...")
# Testing different support values
supports = [0.01, 0.05, 0.1, 0.15]
num_itemsets = []
for s in supports:
    frequent_itemsets = fpgrowth(basket_sets, min_support=s, use_colnames=True)
    num_itemsets.append(len(frequent_itemsets))

plt.figure(figsize=(8, 5))
plt.plot(supports, num_itemsets, marker='o', linestyle='--')
plt.title('Number of Frequent Itemsets vs Minimum Support')
plt.xlabel('Minimum Support')
plt.ylabel('Number of Frequent Itemsets')
plt.grid(True)
plt.savefig('images/support_vs_itemsets.png')
plt.close()

# We choose a reasonable support value, e.g., 0.05
frequent_itemsets = fpgrowth(basket_sets, min_support=0.05, use_colnames=True)
frequent_itemsets.to_csv('outputs/frequent_itemsets.csv', index=False)

# 5. Association Rule Generation
print("Generating association rules...")
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# 6. Rule Filtering and Interpretation
# Filter for meaningful rules
filtered_rules = rules[(rules['lift'] > 1.2) & (rules['confidence'] > 0.3)]
filtered_rules = filtered_rules.sort_values('lift', ascending=False)
filtered_rules.to_csv('outputs/association_rules.csv', index=False)

print(f"Number of filtered rules: {len(filtered_rules)}")

# Save top 15 rules for interpretation
top_rules = filtered_rules.head(15)
top_rules.to_csv('outputs/top_rules.csv', index=False)

# Plot support vs confidence
plt.figure(figsize=(8, 6))
sns.scatterplot(x='support', y='confidence', size='lift', hue='lift', data=filtered_rules, palette='viridis')
plt.title('Association Rules: Support vs Confidence')
plt.savefig('images/rules_scatter.png')
plt.close()

print("Process completed successfully.")
