def chunk_text(text, size=600):
	words = text.split()
	return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]