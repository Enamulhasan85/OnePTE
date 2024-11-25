# OnePTE - PTE Exam Management API

OnePTE is a backend system for managing PTE (Pearson Test of English) exams. It provides RESTful APIs for managing questions of different types including **Summarize Spoken Text (SST)**, **Re-Order Paragraphs (RO)**, and **Reading Multiple Choice Questions (RMMCQ)**, submitting answers, and tracking user practice history. The backend is built using Django REST Framework and integrates with a relational database for data storage.

## Table of Contents

- [Introduction](#onepte---pte-exam-management-api)
- [Installation](#installation)
- [Admin Module](#admin-module)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
    - [POST /api/token/](#1-get-user-access-token)
    - [POST /api/token/refresh/](#2-refresh-user-access-token)
  - [Questions](#questions)
    - [GET /api/questions/](#3-get-questions-list)
    - [GET /api/questions/{id}](#4-get-question-details)
  - [Answers](#answers)
    - [POST /api/submit-answer/](#5-submit-answer)
  - [Practice History](#practice-history)
    - [GET /api/practice-history/](#1-get-practice-history)

## Installation

To get started with this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Enamulhasan85/OnePTE.git
   ```

2. Navigate into the project directory:
   ```bash
    cd onepte
    ```

3. Create a virtual environment 
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   On Windows:
    ```bash
    venv\Scripts\activate
    ```

   On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```bash
   python manage.py runserver
   ```

The application should now be accessible at http://127.0.0.1:8000.


### Frontend Setup and Usage

This section provides instructions for setting up and running the React frontend of the OnePTE project.

1. Ensure that you have **Node.js** and **npm** installed:
  ```bash
  node -v
  npm -v
  ```
2. **Navigate to the frontend directory:**
  Go to the frontend directory (assuming your frontend is inside the `frontend` folder):
  ```bash
  cd onepte-frontend
  ```
3. **Install dependencies:**
  In the frontend directory, run the following command to install all the required dependencies:
  ```bash
    npm install
  ```
  This will install all the dependencies listed in the `package.json` file.

### Running the Development Server

To start the React development server, run the following command:

  ```bash
  npm start
  ```

This will:

- Start the development server.
- Open the application in your default browser (usually at `http://localhost:3000`).

### Running Frontend and Backend Together

To run both the frontend and backend simultaneously:

- Open two terminal windows:
  - One for running the **backend** using `python manage.py runserver`.
  - One for running the **frontend** using `npm start`.

This will allow you to test the full application with both the frontend and backend running.

## Admin Module

The **Admin Module** in the project allows administrators to manage questions, answers, and practice history directly through the Django admin interface. Follow these steps to configure and access the admin panel:

#### 1. **Creating a Superuser**
To access the admin panel, you need to create a superuser account. Run the following command in your terminal:

```bash
python manage.py createsuperuser
```

Provide the required details (username, email, password) when prompted.

#### 2. **Accessing the Admin Panel**
Start the development server and navigate to the admin panel using the following URL:

```plaintext
http://127.0.0.1:8000/admin/
```

Log in using the superuser credentials you created.

#### 3. **Managing Data in the Admin Panel**
The following models are available for management in the admin panel:
- **Questions**: Add, edit, or delete questions.
- **Answers**: View and manage submitted answers.
- **Practice History**: Track and review user practice data.
- **Users**: Manage registered users.

#### 4. **Admin Permissions**
Ensure that only authorized personnel have access to the admin panel. Assign appropriate permissions to admin users based on their roles.

## API Postman Collection

For easier interaction with the API, you can import the following Postman collection:

[OnePTE API Postman Collection](https://api.postman.com/collections/12463439-429d3dce-b10e-4ce4-bf5f-a3d9c4912fbc?access_key=PMAT-01JDENNMJF26PF96T91WJT5NQ4)

You can use this collection to test various API endpoints with example requests and responses.

## API Endpoints

This repository contains the API documentation and usage for the **OnePTE** platform. Below are the key API endpoints used for various operations.

## Authentication

### 1. Get User Access Token
- **Endpoint**: `POST /api/token/`
- **Description**: Retrieves an access token using user credentials (username and password).
- **Request Body**:
  ```json
  {
    "username": "user1",
    "password": "enamD291"
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNDg1ODIzLCJpYXQiOjE3MzI0NDI2MjMsImp0aSI6ImQ0ZDlkODdlY2IxMDQwZDZhMDAzYzEyYjQyYTJiZjgxIiwidXNlcl9pZCI6Mn0.b7VDSR2SxpzYURjGiVsbjD1lbqIfG1IHkSY1hwWcL3I",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzA0NzQyMywiaWF0IjoxNzMyNDQyNjIzLCJqdGkiOiJlZTZhNWI5MGQwMGU0YmM2YTJmMmE0YWMzZGQ5ODYzZSIsInVzZXJfaWQiOjJ9.L5c0O6JoF3hSb3kerByXPhzRBjbUi02Q3qB2ogBj9FY"
  }
  ```

### 2. Refresh User Access Token
- **Endpoint**: `POST /api/token/refresh/`
- **Description**: Refreshes the access token using a valid refresh token.
- **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzAwMjc2MywiaWF0IjoxNzMyMzk3OTYzLCJqdGkiOiJmMzVkNjBiNWQ4NTc0NjBjYWRmY2NkMDgwMzlkMDNhZiIsInVzZXJfaWQiOjJ9.c_J107GlkyK_2ZF9fDC6Tns-J9yT3vbymwgowIM7ULI"
  }
  ```
- **Response**:
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNDg1OTE2LCJpYXQiOjE3MzIzOTc5NjMsImp0aSI6IjNjODJjMzJiZjYwMjRjZTc5ZGVkN2FmNjdlMDJiY2VjIiwidXNlcl9pZCI6Mn0.7UXdCGH-uz1hLgIag_Sw4aY6z51puav1DH-X0_pVqTg",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzA0NzUxNiwiaWF0IjoxNzMyNDQyNzE2LCJqdGkiOiIzODhhODJmN2QzZDU0YzBlOTkyMWQ5NWUyOTU3MWEyYSIsInVzZXJfaWQiOjJ9.RnDzWqM2CGlrWKTXq1FtFW3sgt-moLeOXEQLh3auFk4"
  }
  ```

## Questions

### 3. Get Questions List
- **Endpoint**: `GET /api/questions/`
- **Description**: Retrieves a list of questions filtered by `question_type`. Example: `SST` for Summarize Spoken Text.
- **Query Parameters**:
  - `question_type`: The type of question (e.g., `SST`, `RMMCQ`, `RO`).
  - `page`: The page number for paginated results (optional).
- **Example Request**:
  ```bash
  GET /api/questions/?question_type=SST&page=1
  ```
- **Response**:
  ```json
    {
        "count": 9,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "title": "Summarize the audio clip.",
                "question_type": "SST",
                "question_type_display": "Summarize Spoken Text"
            },
            {
                "id": 4,
                "title": "ttile 1",
                "question_type": "SST",
                "question_type_display": "Summarize Spoken Text"
            },
            {
                "id": 5,
                "title": "title 2",
                "question_type": "SST",
                "question_type_display": "Summarize Spoken Text"
            },
        ]
    }
  ```

### 4. Get Question Details
- **Endpoint**: `GET /api/questions/{id}`
- **Description**: Retrieves the details of a specific question by ID.
- **Example Request**:
  ```bash
  GET /api/questions/3
  ```
- **Response**:
  ```json
    {
        "id": 3,
        "title": "What is the impact of artificial intelligence on industries?",
        "question_type": "RMMCQ",
        "question_type_display": "Reading Multiple Choice (Multiple)",
        "answer_time_limit": null,
        "audios": null,
        "paragraphs": null,
        "passage": "Artificial intelligence (AI) is revolutionizing many industries. From manufacturing to finance, AI is helping businesses automate processes, increase efficiency, and improve decision-making.",
        "options": [
            {
                "id": 1,
                "content": "AI only benefits large corporations."
            },
            {
                "id": 2,
                "content": "AI can help businesses increase efficiency and make better decisions."
            },
            {
                "id": 3,
                "content": "AI has effect on industries"
            }
        ]
    }
  ```

## Answers

### 5. Submit Answer
- **Endpoint**: `POST /api/submit-answer/`
- **Description**: Submits an answer for a specific question.
- **Authentication**: Requires a valid access token (Bearer token).
- **Request Headers**:
  - `Authorization`: `Bearer <access_token>`

- **Request Body**:
  ```json 
  {
    "question_id": "1",
    "answer": "the summary of the audio is..."
  }
  //(SST)
  ``` 
  ```json 
  {
    "question_id": "2",
    "answer": [2, 3, 1]
  }
  //(RO)
  ```
  ```json
  {
    "question_id": "3",
    "answer": [2, 3, 1]
  }
  //(RMMCQ)
  ```
- **Response**:
  ```json 
  {
      "message": "Answer submitted successfully. Your score will be available soon.",
      "data": {
          "id": 34,
          "question_id": 1,
          "question_type": "SST",
          "question_type_display": "Summarize Spoken Text"
      }
  }
  //(SST)
  ``` 
  ```json 
  {
    "message": "Answer submitted successfully.",
    "data": {
      "id": 35,
      "question_id": 2,
      "question_type": "RO",
      "question_type_display": "Re-Order Paragraph",
      "score_components": {
          "Blank": {
              "score": 1,
              "max_score": 2
          }
      }
    }
  }
  //(RO)
  ```
  ```json
  {
    "message": "Answer submitted successfully.",
    "data": {
        "id": 36,
        "question_id": 3,
        "question_type": "RMMCQ",
        "question_type_display": "Reading Multiple Choice (Multiple)",
        "score_components": {
            "Choice": {
                "score": 1,
                "max_score": 2
            }
        }
    }
  }
  //(RMMCQ)
  ```

## Practice History

### 1. Get Practice History
- **Endpoint**: `GET /api/practice-history/`
- **Description**: Retrieves a list of practice history for a specific user.
- **Authentication**: Requires a valid access token (Bearer token).
- **Request Headers**:
  - `Authorization`: `Bearer <access_token>`
- **Query Parameters**:
  - `page`: The page number for paginated results (optional).

- **Example Request**:
```bash
GET /api/practice-history/?page=1
Authorization: Bearer <access_token>
```

- **Response**:
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "question_id": 1,
            "question_title": "Summarize the audio clip.",
            "question_type": "SST",
            "question_type_display": "Summarize Spoken Text",
            "submitted_at": "2024-11-21T10:19:54.193753Z",
            "score": {
                "Content": {
                    "score": 1,
                    "max_score": 2
                },
                "Form": {
                    "score": 1,
                    "max_score": 2
                },
                "Grammar": {
                    "score": 1,
                    "max_score": 2
                },
                "Vocabulary": {
                    "score": 2,
                    "max_score": 2
                },
                "Spelling": {
                    "score": 1,
                    "max_score": 2
                },
                "Total": {
                    "score": 6,
                    "max_score": 10
                }
            }
        },
        {
            "id": 2,
            "question_id": 2,
            "question_title": "Rearrange the following paragraphs in the correct order.",
            "question_type": "RO",
            "question_type_display": "Re-Order Paragraph",
            "submitted_at": "2024-11-22T22:25:13.287990Z",
            "score": {
                "Blank": {
                    "score": 2,
                    "max_score": 2
                }
            }
        },
        {
            "id": 3,
            "question_id": 3,
            "question_title": "What is the impact of artificial intelligence on industries?",
            "question_type": "RMMCQ",
            "question_type_display": "Reading Multiple Choice (Multiple)",
            "submitted_at": "2024-11-23T22:27:10.485746Z",
            "score": {
                "Choice": {
                    "score": 1,
                    "max_score": 2
                }
            }
        },
    ]
}
```

## API Usage

- **Base URL**: `{{BaseURL}}` (e.g., `http://127.0.0.1:8000/`).
- Replace `{{BaseURL}}` with the actual base URL for API requests.

## Notes

- You can use the provided access tokens for authentication in future requests.
- For pagination, use the `page` query parameter where necessary.
- Ensure that the `Authorization` header is provided with a valid `bearer token` when making requests that require user authentication.
