## System Design Documentation: OnePTE Backend

### 1. **Overview**
OnePTE is a backend system designed to manage Pearson Test of English (PTE) exams. It provides RESTful APIs for handling various question types such as Summarize Spoken Text (SST), Re-Order Paragraphs (RO), and Reading Multiple Choice Questions (RMMCQ). The system allows students to practice and submit answers, track their progress, and receive scores. The backend is built using Django REST Framework (DRF) and integrates with a relational database (SQLite) for data storage.

### 2. **System Architecture**

The system follows a standard client-server architecture, where the backend is responsible for handling business logic, data management, and providing APIs to interact with the system. The backend connects to a SQLite database, which stores all relevant data, including user information, questions, answers, and scores. 

The system is divided into three major layers:
- **Presentation Layer**: Responsible for handling API requests from the frontend (students).
- **Business Logic Layer**: Contains the core application logic such as scoring and tracking user progress.
- **Data Layer**: Manages all data storage and retrieval from the SQLite database.

### 3. **Components & Models**

#### 3.1 **Question Model**
- **Purpose**: The central model that represents a question in the system. It includes the title and question type.
- **Fields**:
  - `title`: The title of the question.
  - `question_type`: Specifies the type of the question (SST, RO, RMMCQ).

#### 3.2 **Question Types**
The system supports three types of questions, each with its own model that contains additional details.
- **Summarize Spoken Text (SST)**:  
  - **Purpose**: Stores the details of an SST question, such as the time limit for answering.
  - **Fields**:
    - `answer_time_limit`: The time limit for answering the SST question.
  - **Additional Models**:
    - `SSTAudioFile`: Represents audio files associated with SST questions. Each file is linked to a specific SST question and contains a speaker's name and the audio file itself.
      - Fields: 
        - `sst_question`: The related SST question.
        - `file`: The audio file for the SST question.
        - `speaker_name`: The name of the speaker in the audio.
      
- **Re-Order Paragraph (RO)**:  
  - **Purpose**: Stores the details of a Re-Order Paragraph question.
  - **Fields**: 
    - No additional fields other than the association to the `Question` model.
  - **Additional Models**:
    - `ReorderParagraph`: Represents the paragraphs that can be reordered in the Re-Order Paragraph questions. It contains the content of each paragraph and the correct order of the next paragraph.
      - Fields:
        - `reorder_question`: The related Re-Order Paragraph question.
        - `content`: The content of the paragraph.
        - `correct_next_order`: The correct order of the next paragraph in the sequence.
      
- **Reading Multiple Choice Questions (RMMCQ)**:  
  - **Purpose**: Stores the passage associated with a Reading Multiple Choice Question.
  - **Fields**:
    - `passage`: The passage for the RMMCQ question.
  - **Additional Models**:
    - `RMMCQOption`: Represents the multiple-choice options for the RMMCQ question. Each option can be marked as correct or incorrect.
      - Fields:
        - `rmmcq_question`: The related RMMCQ question.
        - `content`: The text of the multiple-choice option.
        - `is_correct`: A boolean value indicating whether this option is correct.

#### 3.3 **Answer Models**
Answers are associated with questions and store the student's responses. The models for each question type also include scoring mechanisms.

- **Answer**:  
  - **Purpose**: Represents an answer submitted by a user (student) for a specific question.
  - **Fields**:
    - `user`: A foreign key to the `User` model, linking the answer to the student who submitted it.
    - `question`: A foreign key to the `Question` model, linking the answer to the specific question being answered.
    - `created_at`: The timestamp when the answer was created, automatically set to the current time when the answer is submitted.

- **SSTAnswer**: 
  - **Purpose**: Stores the student’s summary text for SST and calculates the score for the summary.
  - **Fields**: 
    - `text`: The student’s summary of the audio.
    - `content_score`, `form_score`, `grammar_score`, `vocabulary_score`, `spelling_score`: Scores for each aspect of the summary.
    - `total_score`: The total score based on the individual components.

- **ROAnswer**: 
  - **Purpose**: Stores the student's order of paragraphs and calculates the score based on correct adjacent pairs.
  - **Fields**: 
    - `paragraph_order`: The student’s submitted order for the paragraphs.
    - `total_score`: Total score based on correct adjacent pairs.

- **RMMCQAnswer**: 
  - **Purpose**: Stores the options selected by the student and calculates the score based on correct and incorrect options.
  - **Fields**: 
    - `selected_options`: The list of options selected by the student.
    - `total_score`: The total score for the question.

### 4. **API Design**

The system exposes RESTful APIs to manage questions, answers, and user progress. The endpoints are designed to be used by the frontend for student interaction.

#### 4.1 **Authentication APIs**  
- **POST /api/token/**  
- **POST /api/token/refresh/**

#### 4.2 **Question APIs**  
- **GET /api/questions/**  
- **GET /api/questions/{id}/**

#### 4.3 **Answer Submission APIs**  
- **POST /api/submit-answer/**

#### 4.5 **Practice History APIs**  
- **GET /api/practice-history/**  

### 5. **Database Design**

The system uses SQLite for data storage. The database schema is designed to support the models outlined above, with foreign key relationships between models where necessary.

- **Question**: The main table to store question details. It is linked to question-specific tables (SST, RO, RMMCQ) through a one-to-one relationship.
- **SST**: Stores SST-specific information, including the answer time limit.
- **RO**: Stores Re-Order Paragraph question details and paragraphs.
- **RMMCQ**: Stores RMMCQ question passages and options.
- **Answer**: Tracks user submissions for each question type.
- **SSTAnswer, ROAnswer, RMMCQAnswer**: Store student answers and associated scores.

### 6. **Scoring Mechanism**

Each question type has its own scoring logic:
- **SST**: Scores are calculated based on five components (content, form, grammar, vocabulary, spelling), each having a maximum score of 2. The total score is the sum of these components (out of 10).  
  **Background Scoring**: To optimize performance, scoring for SST questions is handled asynchronously using threading. This allows the system to perform scoring tasks in the background without blocking the main process, improving user experience and system responsiveness.
- **RO**: The score is based on the number of correct adjacent pairs in the reordered paragraphs.
- **RMMCQ**: Each correct option adds 1 point to the score, while incorrect options subtract 1 point, ensuring the score is non-negative.

### 7. **Security**

- **Authentication**: The system uses Django’s default authentication mechanisms along with JWT and session-based authentication. JWT is used for API-based interactions, while session-based authentication is used for web-based interactions.
- **Authorization**: Access to the API is role-based, with different permissions for students and administrators. Students can access questions, submit answers, and view their scores, while administrators have management access to questions, scores, and user data.
- **Data Validation**: Each API endpoint performs input validation to ensure data integrity and prevent invalid submissions.

### 8. **Conclusion**

The OnePTE system provides a simple, flexible backend for managing PTE exam practice. It supports multiple question types, scoring logic, and user interaction, and is designed to be scalable and extensible for future requirements. With the use of Django REST Framework and SQLite, the system is both efficient and easy to maintain.