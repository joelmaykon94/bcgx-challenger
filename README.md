# BCGX Challenger

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

##### Directory Structure - Clean Architecture V1
```
bcgx-challenger/
│
├── api/
│   ├── requirements.txt            # Dependencies
│   ├── main.py                     # Entry point
│   ├── domain/
│   │   └── models.py               # Database models
│   │   
│   │
│   ├── repositories/
│   │   └── file_repository.py       # Data access layer
│   │
│   ├── usecases/
│   │   └── file_usecases.py         # Business logic
│   │
│   └── framework/
│       ├── database.py              # Database setup
│       └── pdf_utils.py             # PDF extraction utilities
│
└── app/
```


#### **Phase 2:**
- [ ] User questions
- [X] Rank text similarity to user questions
- [ ] Create RAG prompts
  - [ ] 

##### Directory Structure - Clean Architecture V2
```
bcgx-challenger/
│
├── api/
│   ├── requirements.txt            # Dependencies
│   ├── main.py                     # Entry point
│   ├── domain/
│   │   └── models.py               # Database models
│   │   
│   │
│   ├── repositories/
│   │   └── file_repository.py       # Data access layer
│   │
│   ├── usecases/
│   │   └── file_usecases.py         # Business logic
│   │
│   └── framework/
│       ├── database.py              # Database setup
│       └── pdf_utils.py             # PDF extraction utilities
│
└── app/
```

#### **Phase 3:**
- [ ] Initiate dialogue with the LLM
- [ ] Consume API call on streamlit

#### **Phase 4:**
- [ ] Evaluate metrics for context and Q&A
- [ ] Optimize prompts using RAG metrics
- [ ] Upload files with optimized prompts
- [ ] Human review of answers
- [ ] Link to source data for extraction

---

### Execution of the API Locally
1. Clone the repository.
2. Navigate to the directory: `cd bcgx-challenger/api`
3. Install the required libraries: `pip install -r requirements.txt`
4. Run the application: `uvicorn main:app --reload`
5. configure the connection with postgres database `DATABASE_URL` into file bcgx-challenger/api/main.py - reflects the details of a remote database if it is not a localhost database.
6. Access the application at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Run with Docker
1. run command: `docker-compose up --build`
2. Access the application at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Run APP Interface Web
1. install libraries: `pip install streamlit requests`
2. run: `streamlit run app.py`

### Tech and Frameworks
- **[Streamlit](https://streamlit.io/generative-ai)** - Frontend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Backend
- **[Postgres](https://www.postgresql.org/)** - Database
- **[PG Vector](https://github.com/pgvector/pgvector)** - Vector Database

---

### BCG X Squad Five

| ![Hugo](https://github.com/hucodelab.png) | ![Joel Maykon](https://github.com/joelmaykon94.png) | ![Juliana Gonçalves](https://github.com/jungoncalves.png) | ![Mike Futorny](https://github.com/MikeFutorny.png) |
|--------------------------------------------|------------------------------------------------------|------------------------------------------------------------|-------------------------------------------------------|
| [Hugo - Data Engineer](https://github.com/hucodelab) | [Joel Maykon - Data Scientist](https://github.com/joelmaykon94) | [Juliana Gonçalves - Data Scientist](https://github.com/jungoncalves) | [Mike Futorny - Software Engineer](https://github.com/MikeFutorny) |
