import os
import sys
import pandas as pd
import ast

os.chdir(r"C:\Users\KIIT0001\Desktop\analysis folder")
sys.stdout = open('output.txt', 'w', encoding='utf-8')

print("Loading datasets...")

ev1 = pd.read_csv("eve_202603051200000000.csv")
ev2 = pd.read_csv("eve_202603051800000000.csv")
ev3 = pd.read_csv("events_20260406.csv")
events = pd.concat([ev1, ev2, ev3], ignore_index=True)

stories = pd.read_csv("Stories_sample_data.csv", low_memory=False)

print("Datasets loaded!")

if 'timestamp' in events.columns:
    events['hour'] = pd.to_datetime(events['timestamp'], errors='coerce').dt.hour

def clean_id(x):
    if isinstance(x, dict):
        return x.get('$oid') or str(x)
    if isinstance(x, str) and x.startswith('{'):
        try:
            parsed = ast.literal_eval(x)
            return parsed.get('$oid') or str(parsed)
        except:
            pass
    return str(x).strip()

events['entity_id'] = events['entity_id'].apply(clean_id)
stories['_id'] = stories['_id'].apply(clean_id)

def extract_category(cat):
    if isinstance(cat, dict):
        return cat.get('slug') or cat.get('title')
    if isinstance(cat, str) and cat.startswith('{'):
        try:
            parsed = ast.literal_eval(cat)
            return parsed.get('slug') or parsed.get('title')
        except:
            pass
    return str(cat) if pd.notna(cat) else 'unknown'

stories['category_clean'] = stories['category'].apply(extract_category)

def extract_author(x):
    if pd.isna(x) or x == '[]' or x == '':
        return 'unknown'
    if isinstance(x, str) and x.startswith('{'):
        try:
            parsed = ast.literal_eval(x)
            firstname = parsed.get('firstname') or ''
            lastname = parsed.get('lastname') or ''
            full_name = f"{firstname} {lastname}".strip()
            return full_name if full_name else 'unknown'
        except:
            pass
    return 'unknown'

if 'author_details' in stories.columns:
    stories['author_clean'] = stories['author_details'].apply(extract_author)
elif 'primary_author_details' in stories.columns:
    stories['author_clean'] = stories['primary_author_details'].apply(extract_author)
else:
    stories['author_clean'] = 'unknown'

stories_slim = stories[['_id', 'category_clean', 'author_clean']].copy()

df = events.merge(
    stories_slim,
    left_on='entity_id',
    right_on='_id',
    how='inner'
)

print(f"Merged rows: {df.shape[0]}")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("\n Q1: Author Views ")
author_views = df.groupby('author_clean').size().sort_values(ascending=False)
print("\nAll authors by views (highest to lowest):")
print(author_views.to_string())
print(f"\nHighest: {author_views.index[0]} — {author_views.iloc[0]:,} views")
print(f"Lowest:  {author_views.index[-1]} — {author_views.iloc[-1]:,} views")

print("\n Q2: Hourly Distribution ")
print("\nSessions per hour:")
print(events.groupby('hour')['session_id'].nunique().to_string())
print("\nEvents per hour:")
print(events.groupby('hour').size().to_string())

print("\n Q3: Most and Least Viewed Content Types ")
cat_views = df.groupby('category_clean').size().sort_values(ascending=False)
print("\nAll content types by views (highest to lowest):")
print(cat_views.to_string())
print(f"\nMost viewed:  {cat_views.index[0]} — {cat_views.iloc[0]:,} views")
print(f"Least viewed: {cat_views.index[-1]} — {cat_views.iloc[-1]:,} views")

print("\n Q4: User Distribution % ")
if 'user_type' in events.columns:
    print(events['user_type'].value_counts(normalize=True).mul(100).round(2).to_string())

print("\n Q5: Category-wise Story Distribution % ")
cat_dist = df['category_clean'].value_counts(normalize=True).mul(100).round(4)
print(cat_dist.to_string())

print("\n Q6: Total Views per Category ")
print(df.groupby('category_clean').size().sort_values(ascending=False).to_string())

print("\n--- Q7: Dominant Category per Hour ---")
temp = df.groupby(['hour', 'category_clean']).size().reset_index(name='count')
dominant = temp.loc[temp.groupby('hour')['count'].idxmax()]
print(dominant.to_string())

print("\n Q8: Average Scroll Depth by Category ")
if 'scroll_depth' in df.columns:
    print(df.groupby('category_clean')['scroll_depth'].mean().sort_values(ascending=False).to_string())
else:
    print(" scroll_depth not found")

print("\n Q9: Total Views per Story ")
print(df.groupby('entity_id').size().sort_values(ascending=False).to_string())

print("\n Q10: Average Read Time by Category ")
if 'engagement_time' in df.columns:
    print(df.groupby('category_clean')['engagement_time'].mean().sort_values(ascending=False).to_string())
elif 'engagement_time' in events.columns:
    print(events.groupby('hour')['engagement_time'].mean().to_string())
else:
    print(" engagement_time column not found in dataset — cannot calculate read time")

print("\n ANALYSIS COMPLETE")