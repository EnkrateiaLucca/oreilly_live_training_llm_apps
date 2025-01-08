Guide to Optimal Chunk Size for RAG Applications

# Introduction
When developing Retrieval-Augmented Generation (RAG) systems with large language models (LLMs), determining the right chunk size is a crucial balance between retrieval accuracy, computational efficiency, and response quality. This guide provides an overview of chunking principles, strategies, and factors influencing chunk size selection to optimize the performance of RAG systems.

Chunking in RAG Systems Chunking involves dividing documents into smaller, manageable pieces ("chunks") for processing and retrieval. Effective chunking helps enhance the relevance of retrieved information, ensuring that LLMs generate coherent, contextually accurate responses. Selecting the right chunk size ensures that chunks are both informative and computationally efficient, maintaining semantic integrity.

# Strategies for Determining Optimal Chunk Size

[Fixed-Size Chunking/Naive Chunking](https://ar5iv.labs.arxiv.org/html/2401.07883): Splitting text by a set word or token count is straightforward but may disrupt semantic units, leading to fragmented or less coherent responses.

[Semantic Chunking](https://arc.net/l/quote/erghdulb): Using natural language processing tools to divide the text at logical boundaries preserves meaning and helps the LLM produce more coherent outputs.

[Adaptive Chunking](https://vectify.ai/blog/LargeDocumentSummarization?utm_source=substack&utm_medium=email): Adjusting chunk size based on the document’s length and structure balances consistency across chunks, optimizing both retrieval and generation.
# Factors Influencing Chunk Size Selection

LLM Context Window: LLMs are limited by a fixed context window size, such as 4k or 8k tokens. To use this full context effectively without truncation, chunks must be small enough to fit within the model's window.

Embedding Model Constraints: Embedding models also have context length limitations. Chunks must fit these constraints to ensure accurate similarity searches during retrieval.

Document Structure and Content: The coherence of the text is critical. Chunks should ideally align with natural boundaries—such as sentences or paragraphs—to maintain the meaning and coherence of the original document.

Retrieval Precision vs. Recall: Smaller chunks can improve precision, providing highly relevant segments, but may require more retrievals to complete a response, affecting recall. Larger chunks may improve recall but risk introducing less relevant information.

Overlap Between Chunks: Introducing overlaps between chunks helps maintain context at the boundaries, which is essential when the context crosses chunk borders, thereby improving retrieval accuracy.

Computational Efficiency: Smaller chunks lead to increased retrieval operations and embedding computations, which adds to the computational cost. Balancing chunk size to reduce the retrieval load while ensuring good response quality is essential.

Domain-Specific Requirements: Technical documents might benefit from larger chunks (e.g., entire sections) for completeness, while conversational data might require more granular, smaller chunks for precision.

# A Rough Intuitive Guide for Finding Optimal Chunk Size
 
 1. [Consider task’s property](https://arc.net/l/quote/tpizvina): Different tasks may benefit from different kinds of retrieval chunks. For example, question-answer tasks may prefer short phrases, while summarization tasks may prefer long documents.
 2. [Encoder’s property. Different encoder models have varying encoding capabilities on texts with different lengths. For example, models in the sentence-transformer (Reimers and Gurevych, 2019) behave better on a single sentence, while the text-embedding-ada-002 (OpenAI, 2022) is good at longer texts.](https://arc.net/l/quote/spmjsukq)
	 1. In general we'll use [llm-based encoders](https://arc.net/l/quote/fznujufc)
 3. [(3) Query’s property. The length of the user’s queries should be aligned with the chunking size, which implicitly aligns the amount of contextual information in chunks with that in queries, thus improving the relevance between queries and retrievals. For example, a retrieval database built on short phrases may be useless for queries with long documents.](https://arc.net/l/quote/wymtpkmo)
 4. Experimentation: Experiment with different chunk sizes to identify what works best for your specific application and dataset. Tools like LlamaIndex can assist in assessing chunking strategies.
 5. Monitor Metrics: Regularly evaluate metrics like retrieval accuracy, response coherence, and computational efficiency. Adjust your chunking strategy as required to improve performance.
 6. Context Window Limits: Ensure the total tokens (retrieved text plus prompt) fit within the LLM’s context window. This allows the LLM to process multiple chunks simultaneously, enhancing contextual richness.
 7. Semantic Completeness: Make chunks self-contained units of meaning—ideally whole paragraphs or logical segments—to help maintain semantic integrity during retrieval and generation.
 8. Information Density: Balance information density and conciseness. Chunks should have enough information to convey a complete idea but remain manageable for the model’s context window. A typical range is 100-300 tokens, depending on the data type.


# Resources
- https://zilliz.com/blog/exploring-rag-chunking-llms-and-evaluations
- [Optimal chunk size for Large Document Summarization](https://vectify.ai/blog/LargeDocumentSummarization?utm_source=substack&utm_medium=email)
- https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5
- https://antematter.io/blogs/optimizing-rag-advanced-chunking-techniques-study
- https://www.analyticsvidhya.com/blog/2024/10/chunking-techniques-to-build-exceptional-rag-systems/
- https://www.databricks.com/blog/long-context-rag-performance-llms
- https://www.datacamp.com/tutorial/how-to-improve-rag-performance-5-key-techniques-with-examples
- https://chatgen.ai/blog/the-ultimate-guide-on-chunking-strategies-rag-part-3/
- https://developer.ibm.com/articles/awb-retrieval-augmented-generation-rag-with-llms-from-watsonx
- https://docs.mistral.ai/guides/rag/
- https://www.rungalileo.io/blog/mastering-rag-advanced-chunking-techniques-for-llm-applications
- https://unstructured.io/blog/chunking-for-rag-best-practices
- https://mallahyari.github.io/rag-ebook/04_advanced_rag.html
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase
- [RAG Survey](https://ar5iv.labs.arxiv.org/html/2407.13193)
- [RAG for financial documents and recursive chunking strategies](https://ar5iv.labs.arxiv.org/html/2404.07221)
- [Mix-of-Granularity: Optimize the Chunking Granularity for Retrieval-Augmented Generation]()
- [[NAIVE RAG Overview]]
