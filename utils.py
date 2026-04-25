def chunk_text_with_overlap(text, size=500, overlap=100):
    chunk_text=[]
    for i in range(0, len(text), size-overlap):
        chunk_text.append(text[i:i+size])
    return chunk_text