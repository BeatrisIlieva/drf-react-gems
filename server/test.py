import re

def filter_chunk_with_most_keywords(keywords, k=10):
    relevant_chunks = [
        'Collection: Daisy; Color: Green; Metal: Platinum; Stone: Aquamarine; Category: earring; Product ID: 26; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746121011/3_uskksz.webp; Sizes: Size: Small - Price: $4413.00,Size: Medium - Price: $4523.00,Size: Large - Price: $4637.00; Average Rating: 3.8/5 stars;',
        'Collection: Daisy; Color: Green; Metal: Gold; Stone: Aquamarine; Category: earring; Product ID: 27; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746121011/3_uskksz.webp; Sizes: Size: Small - Price: $4413.00,Size: Medium - Price: $4523.00,Size: Large - Price: $4637.00; Average Rating: 3.8/5 stars;',
        
    ]
    
    if not relevant_chunks:
        return None
    
    # Split keywords into list
    keyword_list = keywords.split()
    
    # For each chunk, count exact keyword occurrences (case-insensitive whole word match)
    chunk_scores = []
    for chunk in relevant_chunks:
        chunk_text_lower = chunk.lower()
        score = sum(1 for keyword in keyword_list if re.search(r'\b{}\b'.format(re.escape(keyword.lower())), chunk_text_lower, re.IGNORECASE))
        chunk_scores.append((chunk, score))
    
    # Filter chunks with at least one keyword match
    valid_chunks = [(chunk, score) for chunk, score in chunk_scores if score > 0]
    
    # If no chunks have any matches, return None
    if not valid_chunks:
        return None
    
    # Find the chunk with the maximum score
    max_chunk = max(valid_chunks, key=lambda x: x[1])[0]
    
    return max_chunk

# Example usage
keywords = "ring green gold sapphire"
best_chunk = filter_chunk_with_most_keywords(keywords)
if best_chunk:
    print("Best matching chunk:")
    print(best_chunk)
else:
    print("No matching chunks found.")
    
    
        # 'Collection: Myosotis; Color: Pink; Metal: Platinum; Stone: Sapphire; Category: Ring; Product ID: 21; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746115871/19_cp3mbf.webp; Sizes: Size: Small - Price: $2816.00,Size: Medium - Price: $2929.00,Size: Large - Price: $3036.00; Average Rating: 4.2/5 stars;',
        # 'Collection: Myosotis; Color: Pink; Metal: Platinum; Stone: Sapphire; Category: Earring; Product ID: 20; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746115871/19_cp3mbf.webp; Sizes: Size: Small - Price: $2816.00,Size: Medium - Price: $2929.00,Size: Large - Price: $3036.00; Average Rating: 4.2/5 stars;',
    # 'Collection: Daisy; Color: Red; Metal: Platinum; Stone: Ruby; Category: Earring; Product ID: 11; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746121145/7_nvuh9g.webp; Sizes: Size: Small - Price: $1717.00,Size: Medium - Price: $1828.00,Size: Large - Price: $1932.00; Average Rating: 4.2/5 stars;',
    #     'Collection: Daisy; Color: Yellow; Metal: Platinum; Stone: Sapphire; Category: Necklace; Product ID: 10; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746121005/5_mvon0h.webp; Sizes: Size: Small - Price: $4405.00,Size: Medium - Price: $4520.00,Size: Large - Price: $4632.00; Average Rating: 4.5/5 stars;',
    #     'Collection: Daisy; Color: Pink; Metal: Platinum; Stone: Sapphire; Category: Earring; Product ID: 19; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746121005/9_sciejy.webp; Sizes: Size: Small - Price: $1509.00,Size: Medium - Price: $1620.00,Size: Large - Price: $1724.00; Average Rating: 4.2/5 stars;',
    #     'Collection: Daisy; Color: Yellow; Metal: Platinum; Stone: Sapphire; Category: Earring; Product ID: 2; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746121009/13_mjvoux.webp; Sizes: Size: Small - Price: $1503.00,Size: Medium - Price: $1613.00,Size: Large - Price: $1727.00; Average Rating: 4.2/5 stars;',
    #     'Collection: Bracelet; Color: Pink; Metal: Platinum; Stone: Sapphire; Category: Watch; Product ID: 3; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746196508/1_zaou5v.png; Sizes: Size: Small - Price: $14906.00,Size: Medium - Price: $15014.00,Size: Large - Price: $15126.00; Average Rating: 4.0/5 stars;',
    #     'Collection: Myosotis; Color: Pink; Metal: Platinum; Stone: Sapphire; Category: Necklace; Product ID: 30; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746115871/7_bxav8b.avif; Sizes: Size: Small - Price: $6704.00,Size: Medium - Price: $6809.00,Size: Large - Price: $6913.00; Average Rating: 3.8/5 stars;',
    #     'Collection: Lotus; Color: Blue; Metal: Platinum; Stone: Sapphire; Category: Necklace; Product ID: 15; Image URL: https://res.cloudinary.com/dpgvbozrb/image/upload/v1746115854/11_grxxeo.webp; Sizes: Size: Small - Price: $7411.00,Size: Medium - Price: $7528.00,Size: Large - Price: $7645.00; Average Rating: 3.7/5 stars;'