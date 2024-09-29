**Implementation Approaches**

1. LangChain (GraphCypherQAChain & GraphQAChain)
1. Llama Index
1. Neo4j Graph RAG
1. Microsoft Graph RAG
1. Triplex, etc

**Difficulties**
1. Local vs Cloud
1. Chunk Strategies
1. LLMs capabilities
1. Custom prompt Strategies

**Explored LLMs**
1. Mistral AI: mistral v0.3 & mistral-nemo   .`Seems good for French docs.`
1. OpenAI GPTs: 3.5-turbo, 4, 4o-mini
1. Meta Llama: 3.1, 3.2 (1b & 3b)
1. Google: Gemma 2 (2b, 9b & 27b)

**Microsoft Graph RAG tests**

```bash
(.venv) emmanuelkoupoh@192 ollama-MS-GraphRAG % python3 -m graphrag.index --root ./rag
```

```plaintext
Logging enabled at 
/Users/emmanuelkoupoh/Documents/Github/ollama-MS-GraphRAG/rag/output/indexing-engine.log

🚀 create_base_text_units
                                 id  ... n_tokens
0  cb57b587e0534208a20768384bf31690  ...      700
1  e454ef64847a598ba409bbf62720e545  ...      126

[2 rows x 5 columns]
🚀 create_base_extracted_entities
                                        entity_graph
0  <graphml xmlns="http://graphml.graphdrawing.or...
🚀 create_summarized_entities
                                        entity_graph
0  <graphml xmlns="http://graphml.graphdrawing.or...
🚀 create_base_entity_graph
   level                                    clustered_graph
0      0  <graphml xmlns="http://graphml.graphdrawing.or...

🚀 create_final_entities
                                 id  ...                              description_embedding
0  d8d44053bf6640e3b1a89c1a6cfff639  ...  [0.8957865238189697, 1.4908967018127441, -4.19...
1  1ca00f1680f840169a42bae2a44b9b4e  ...  [0.7717753052711487, 1.2422819137573242, -3.77...
2  4dc9dd76e3644353a42fe1e592d377b0  ...  [1.2970409393310547, 1.3151257038116455, -3.51...
3  deb850a2bb324d369b5dcc2ba6ddcd3a  ...  [0.9291163682937622, 1.3662649393081665, -3.68...
4  bfe7cbe6f5e74d56a3d55156ef75d89c  ...  [0.2896462082862854, 0.1849261224269867, -3.18...
5  b449d6398d9543a9833cf7ea873c17c8  ...  [0.7374058961868286, 1.574608564376831, -4.143...

[6 rows x 8 columns]

🚀 create_final_nodes
   level          title    type  ...                 top_level_node_id  x  y
0      0    NONNA LUCIA  PERSON  ...  d8d44053bf6640e3b1a89c1a6cfff639  0  0
1      0          AMICO  PERSON  ...  1ca00f1680f840169a42bae2a44b9b4e  0  0
2      0       CAPONATA   EVENT  ...  4dc9dd76e3644353a42fe1e592d377b0  0  0
3      0    FRESH PASTA   EVENT  ...  deb850a2bb324d369b5dcc2ba6ddcd3a  0  0
4      0  CARUSO FAMILY          ...  bfe7cbe6f5e74d56a3d55156ef75d89c  0  0
5      0         SICILY          ...  b449d6398d9543a9833cf7ea873c17c8  0  0

[6 rows x 15 columns]
🚀 create_final_communities
  id        title  level                    relationship_ids                       text_unit_ids
0  0  Community 0      0    
🚀 create_final_relationships
          source  target  weight  ... source_degree target_degree rank
0  CARUSO FAMILY  SICILY     1.0  ...             1             1    2

[1 rows x 10 columns]
🚀 create_final_text_units
                                 id  ...                    relationship_ids
0  cb57b587e0534208a20768384bf31690  ...                                None
1  e454ef64847a598ba409bbf62720e545  ...  

[2 rows x 6 columns]
🚀 create_final_community_reports
  community  ...                                    id
0         0  ...  8024c0d4-56aa-4f43-8de4-a30414316190

[1 rows x 10 columns]

🚀 create_base_documents
                                 id  ...               title
0  94c60d975cb0c44efc50495ff2e9506f  ...  dummytext copy.txt

[1 rows x 4 columns]
🚀 create_final_documents
                                 id  ...               title
0  94c60d975cb0c44efc50495ff2e9506f  ...  dummytext copy.txt

[1 rows x 4 columns]


⠦ GraphRAG Indexer 
├── Loading Input (InputFileType.text) - 1 files loaded (1 filtered) ━━━━━━━━━━━━━ 100% 0:00:00 0:00:00
├── create_base_text_units
├── create_base_extracted_entities
├── create_summarized_entities
├── create_base_entity_graph
├── create_final_entities
├── create_final_nodes
├── create_final_communities
├── create_final_relationships
├── create_final_text_units
├── create_final_community_reports
├── create_base_documents
└── create_final_documents
🚀 All workflows completed successfully.
```

```bash
(.venv) emmanuelkoupoh@192 ollama-MS-GraphRAG % python -m graphrag.query \             
    --root ./rag \
    --method global \
    "What are the top themes in this story?"

```

```plaintext
creating llm client with {'api_key': 'REDACTED,len=9', 'type': "openai_chat", 'model': 'llama3.1', 'max_tokens': 4000, 'temperature': 0.0, 'top_p': 1.0, 'n': 1, 'request_timeout': 6000000.0, 'api_base': 'http://localhost:11434/v1', 'api_version': None, 'organization': None, 'proxy': None, 'cognitive_services_endpoint': None, 'deployment_name': None, 'model_supports_json': True, 'tokens_per_minute': 0, 'requests_per_minute': 0, 'max_retries': 10, 'max_retry_wait': 10.0, 'sleep_on_rate_limit_recommendation': True, 'concurrent_requests': 25}
```

SUCCESS: Global Search Response:
**Top Themes**

Based on the analysts' reports, the following are the top themes that emerge from the dataset:

### **1. Vulnerability to Threats**

The Sicilian Culinary Community is vulnerable to threats from events like Caponata and Fresh Pasta [Data: Reports (3)]. These events can disrupt the community's dynamics and impact its traditions.

### **2. Importance of Culinary Traditions**

The community's focus on culinary traditions makes it a target for threats [Data: Reports (1, 2)]. The Caruso family's culinary traditions are at the center of the community, highlighting their significance.

### **3. Community Dynamics**

Culinary events like Caponata and Fresh Pasta can be a source of conflict within the community due to their impact on dynamics between entities [Data: Reports (1, 2)].

These themes provide insight into the complexities of the Sicilian Culinary Community and its relationships with external factors.


