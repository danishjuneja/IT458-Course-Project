# Import necessary libraries
import ir_datasets
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Load the dataset
dataset = ir_datasets.load("beir/webis-touche2020/v2")

# Step 2: Preprocess the text data
documents = [query.text for query in dataset.queries_iter()]

# Step 3: Create a vocabulary of unigrams and bigrams
# You can adjust the parameters of CountVectorizer as needed
vectorizer_unigram = CountVectorizer(ngram_range=(1, 1))
vectorizer_bigram = CountVectorizer(ngram_range=(1, 2))

# Fit and transform the documents to create BoW representations
X_unigram = vectorizer_unigram.fit_transform(documents)
X_bigram = vectorizer_bigram.fit_transform(documents)

# Step 4: Calculate the BoW representation for each document

# Get the vocabulary for unigrams and bigrams
vocab_unigram = vectorizer_unigram.get_feature_names_out()
vocab_bigram = vectorizer_bigram.get_feature_names_out()

# Convert BoW representations to dense arrays for analysis
X_unigram_dense = X_unigram.toarray()
X_bigram_dense = X_bigram.toarray()

# Step 5: Compare and analyze the two corpus representations

# Calculate sparsity
sparsity_unigram = 1 - (np.count_nonzero(X_unigram_dense) / np.prod(X_unigram_dense.shape))
sparsity_bigram = 1 - (np.count_nonzero(X_bigram_dense) / np.prod(X_bigram_dense.shape))

# Print sparsity results
print("Sparsity for Unigram BoW:", sparsity_unigram)
print("Sparsity for Bigram BoW:", sparsity_bigram)

# Analyze spatial context (co-occurrence) for unigrams and bigrams
# Find the most common bigrams
bigram_counts = np.sum(X_bigram_dense, axis=0)
most_common_bigrams = [(vocab_bigram[i], bigram_counts[i]) for i in np.argsort(bigram_counts)[::-1][:10]]

print("\nTop 10 most common bigrams:")
for bigram, count in most_common_bigrams:
    print(f"{bigram}: {count}")
