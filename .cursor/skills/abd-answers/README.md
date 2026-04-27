# abd-answers agent

An agent you can deploy in VSCode that allows your AI to have conversational access to Agile by Design's complete Assets area on One Drive. Uses a Pinecone vector database and search. Answers questions grounded our content, includes source citations.

Use it alongside other agents or skills when you need RAG-backed context from the ABD knowledge base (e.g. "what does ABD say about thin slicing?" or "who is better at agile consultng Taimur or Sean?").

You can aslo use the skill to point it to any training materials, engagement deliverables, books, or any document set — it converts source files to markdown, chunks them, embeds them into the Pinecone data store a

## Install

```powershell
cd <your-workspace>/.agents/abd-answers
powershell -ExecutionPolicy Bypass -File Install-Agent.ps1
```

Then edit `conf/.secrets` with your `OPENAI_API_KEY`, `PINECONE_API_KEY`, and `PINECONE_INDEX`.  //one currently provide but may expire

## Quick test

```bash
npm run rag:query -- "what is story mapping" --k 3
```