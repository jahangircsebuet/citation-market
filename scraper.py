from scholarly import scholarly

# Step 1: Search for an author
search_query = scholarly.search_author("John Doe")  # Replace with the actual name
author = next(search_query)

print(author)

# # Step 2: Fill in the author's full profile (includes citations, h-index, publications)
# author_filled = scholarly.fill(author)

# # Print basic profile information
# print(f"Name: {author_filled['name']}")
# print(f"Affiliation: {author_filled['affiliation']}")
# print(f"Total Citations: {author_filled['citedby']}")
# print(f"h-index: {author_filled['hindex']}")
# print(f"i10-index: {author_filled['i10index']}")
# print("Citations per year:")
# for year, count in author_filled['cites_per_year'].items():
#     print(f"{year}: {count}")

# # Step 3: Get list of publications
# print("\nTop Publications:")
# for i, pub in enumerate(author_filled['publications'][:5]):  # Limit to top 5
#     pub_filled = scholarly.fill(pub)
#     title = pub_filled.get('bib', {}).get('title', 'N/A')
#     year = pub_filled.get('bib', {}).get('pub_year', 'N/A')
#     citations = pub_filled.get('num_citations', 0)
#     print(f"{i+1}. {title} ({year}) - {citations} citations")



