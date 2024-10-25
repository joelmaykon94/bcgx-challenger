# BCGX Challenger
### Requirements
* Operating System: Linux or Windows (macOS not tested)
* Docker
* Docker Compose
### Run with Docker
**After clone this repository:**

1. Duplicate the .env.dev file into the root, api, and app directories, renaming it to .env. Then, add your OpenAI API key to the OPENAI_API_KEY field in the .env file located in the api directory.
2. run command: `docker-compose up --build`
3. Access **Eco Docs A.I Web App** at: [http://localhost:8501](http://localhost:8501/)
4. Access **Eco Docs A.I Web API** at: [http://localhost:8000/docs](http://localhost:8000/docs)

### The Mission

#### **Phase 1:**
- [X] Upload files
  - [X] Write I/O temporary file
  - [X] Read I/O memory file
  - [X] Write I/O file into database
- [X] Extract text
- [X] Generate embeddings
- [X] Store in a vector database
- [X] Retrieve similar phrases related to the question
#### **Phase 2:**
- [X] Rank text similarity to user questions
- [X] Create RAG prompts
- [X] Clean text extract
- [x] Validate params of LLM - GPT
- [x] Optimized context and prompt
#### **Phase 3:**
- [X] Create web app with streamlit
- [x] Initiate dialogue with the LLM
- [x] Consume API call on streamlit
#### **Phase 4:**
- [x] Upload files with optimized prompts

### Question [Eco Docs A.I](http://localhost:8501)
Suggested questions as examples to test the app, the list of questions is in the PDF file: [Questions dataset](.assets/question_test_dataset.pdf)

![video](./assets/video_ecodocs_ia.gif)

---
### Tech and Frameworks
- **[Streamlit](https://streamlit.io/generative-ai)** - Frontend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Backend
- **[Weaviate](https://weaviate.io/)** - Vector Database AI-native
- **[Embbeding](https://weaviate.io/developers/weaviate/model-providers/transformers/embeddings)** - Hugging Face Transformers
---

### Project Architecture
![api](./assets/ARCH_ECODOCS.png)


### Weaviate's integration with the Hugging Face Transformers library 
![image](https://weaviate.io/assets/images/integration_transformers_embedding-c322f71d4ed11efa507ca71b1e344b5b.png)
---

___
### BCG X Squad Five

| ![Hugo](https://github.com/hucodelab.png) | ![Joel Maykon](https://github.com/joelmaykon94.png) | ![Juliana Gonçalves](https://github.com/jungoncalves.png) | ![Mike Futorny](https://github.com/MikeFutorny.png) |
|--------------------------------------------|------------------------------------------------------|------------------------------------------------------------|-------------------------------------------------------|
| [Hugo - Data Engineer](https://github.com/hucodelab) | [Joel Maykon - Data Scientist](https://github.com/joelmaykon94) | [Juliana Gonçalves - Data Scientist](https://github.com/jungoncalves) | [Mike Futorny - Software Engineer](https://github.com/MikeFutorny) |
