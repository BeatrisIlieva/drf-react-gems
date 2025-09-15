chunk_objects.append(
    Document(
        page_content=contextualized_chunk,
        metadata={
            'id': f"chunk_{i+1}",
            'length': len(contextualized_chunk),
            'chunk_index': i,
            'total_chunks': len(chunks),
        }
    )
)
