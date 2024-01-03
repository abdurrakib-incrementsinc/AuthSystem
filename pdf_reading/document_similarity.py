import nltk
import gensim
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
# Download the 'punkt' resource
nltk.download('punkt')
import os


def document_token(path1, path2):
    file_docs = []

    # open file and tokenize sentences
    with open(path1) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file_docs.append(line)
    print("file docs ...", file_docs)

    # tokenize words and create dictionary
    gen_docs = [[word.lower() for word in word_tokenize(text)]
                for text in file_docs]
    print("gen docs ...", gen_docs)
    dictionary = gensim.corpora.Dictionary(gen_docs)
    print("dictionary...", dictionary)

    # create a bag of words
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    # TFIDF
    # words that occur frequently across the documents get smaller weights
    tf_idf = gensim.models.TfidfModel(corpus)
    app_base_dir = os.path.dirname(os.path.abspath(__file__))
    sims = gensim.similarities.Similarity(app_base_dir,
                                          tf_idf[corpus],
                                          num_features=len(dictionary))
    # creating query documents
    file2_docs = []
    # open file and tokenize sentences
    with open(path2) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file2_docs.append(line)
    print("file2_docs:", file2_docs)
    # query_docs = [[word.lower() for word in word_tokenize(text)]
    #             for text in file2_docs]
    # query_doc_bow = [dictionary.doc2bow(query_doc) for query_doc in query_docs]
    total_similarity = 0
    for line in file2_docs:
        query_docs = [word.lower() for word in word_tokenize(line)]
        query_doc_bow = dictionary.doc2bow(query_docs)
        query_doc_tf_idf = tf_idf[query_doc_bow]
        print(sims[query_doc_tf_idf])
        total_similarity += np.sum(sims[query_doc_tf_idf])
    total_percentage_similarity = (total_similarity / len(file2_docs)) * 100
    print(f'Total Percentage Similarity: {total_percentage_similarity:.2f}%')


