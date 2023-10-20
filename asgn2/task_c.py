import ir_datasets
import pickle
import numpy as np

# Load the vocabulary
with open('vocabulary.pkl', 'rb') as file:
    loaded_vocabulary = pickle.load(file)

# Load the dataset
dataset = ir_datasets.load("beir/webis-touche2020/v2")


def calculate_df(term):
    # Initialize the document frequency
    df = 0

    # Iterate over the documents in the dataset
    for doc in dataset.docs_iter():
        # Convert the document into a list of terms
        document_terms = doc.text.split()

        # If the term is in the document, increment the document frequency
        if term in document_terms:
            df += 1

    return df

# Define the BM11 and BM15 functions
def bm11(query, document, vocabulary, k1=1.2, b=0.75):
    # Convert the query and document into lists of terms
    query_terms = query.split()
    document_terms = document.split()

    # Calculate document length
    doc_length = len(document_terms)

    # Calculate the average document length
    avg_doc_length = np.mean([len(doc.text.split()) for doc in dataset.docs_iter()])

    # Initialize the BM11 score
    bm11_score = 0

    for term in query_terms:
        if term in vocabulary:
            # Calculate the document frequency
            df = calculate_df(term)

            # Calculate the inverse document frequency
            idf = np.log((dataset.docs_count() - df + 0.5) / (df + 0.5))

            # Calculate the term frequency
            tf = document_terms.count(term)

            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_length / avg_doc_length)

            # Update the BM11 score
            bm11_score += idf * numerator / denominator

    return bm11_score

def bm15(query, document, vocabulary, k1=1.2, b=0.75, delta=0.25):
    # Convert the query and document into lists of terms
    query_terms = query.split()
    document_terms = document.split()

    # Calculate document length
    doc_length = len(document_terms)

    # Calculate the average document length
    avg_doc_length = np.mean([len(doc.text.split()) for doc in dataset.docs_iter()])

    # Initialize the BM15 score
    bm15_score = 0

    for term in query_terms:
        if term in vocabulary:
            # Calculate the document frequency
            df = calculate_df(term)

            # Calculate the inverse document frequency
            idf = np.log((dataset.docs_count() - df + 0.5) / (df + 0.5))

            # Calculate the term frequency
            tf = document_terms.count(term)

            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * doc_length / avg_doc_length)

            # Update the BM15 score
            bm15_score += idf * (numerator / denominator + delta)

    return bm15_score

# Iterate over the documents and queries in the dataset
ctr = 0

for doc, query in zip(dataset.docs_iter(), dataset.queries_iter()):
    # print the doc text and query text
    if ctr < 45:
        ctr += 1
        continue

    print('-------------------')
    # print the first 400 characters of the doc text
    print("Doc: ", doc.text[:500], "...\n")
    print("Query: ", query.text, "\n")

    bm11_score = bm11(query.text, doc.text, loaded_vocabulary)
    bm15_score = bm15(query.text, doc.text, loaded_vocabulary)

    print(f'BM11 Score: {bm11_score}')
    print(f'BM15 Score: {bm15_score}\n')

    ctr += 1

    if ctr == 47:
        break

