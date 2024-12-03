# **Student Management System**

This is a FastAPI-based project for managing student records. It provides RESTful APIs for creating, reading, updating, and deleting student records, with MongoDB as the database. The system is modular and scalable, designed for real-world usage.

## **Features**

- Create a new student record.
- Retrieve a list of students with optional filters (e.g., by country or minimum age).
- Fetch details of a specific student by ID.
- Update student information by ID.
- Delete a student record by ID.
- Built-in exception handling with configurable messages.

## **Prerequisites**

Before running this project, ensure you have the following installed:

1. **Python 3.8 or later**
2. **MongoDB Atlas or a locally hosted MongoDB instance**
3. **pip** (Python package manager)

---

## **Setup Instructions**

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/ReesavGupta/s-m-s-python

cd student-management-system
```

### **2. Set Up a Virtual Environment**

Create and activate a `virtual environment`:

- **On Linux/Mac**:

  ```bash
  python3 -m venv env

  source env/bin/activate
  ```

- **On Windows**:

  ```bash
  python -m venv env

  .\env\Scripts\activate
  ```

### **3. Install Dependencies**

Install the required Python libraries:

- ```bash
  pip install -r requirements.txt
  ```

### **4. Configure Environment Variables**

Create a `.env` file in the root directory with your MongoDB connection string:

- ```env
  MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
  ```
  Replace `username`, `password`, and `dbname` with your MongoDB credentials.

### **5. Run the Application**

Start the FastAPI server:

- ```bash
    python main.py
  ```
  By default, the server will run on http://127.0.0.1:8000.

### **6. Example API Requests**

- #### 1. Create Student

  POST `/student`

  ```json
  {
    "name": "John Doe",
    "age": 25,
    "address": {
      "city": "New York",
      "country": "USA"
    }
  }
  ```

  Response:

  ```json
  {
    "id": "64e8f7b929b9bc3eb5f1d62b"
  }
  ```

- #### 2. List Students

  GET `/students?country=USA&age=20`

  Response:

  ```json
  {
    "data": [
      {
        "id": "64e8f7b929b9bc3eb5f1d62b",
        "name": "John Doe",
        "age": 25,
        "address": {
          "city": "New York",
          "country": "USA"
        }
      }
    ]
  }
  ```

- #### 3. Fetch Student by ID

  GET `/students/64e8f7b929b9bc3eb5f1d62b`

  Response:

  ```json
  {
    "id": "64e8f7b929b9bc3eb5f1d62b",
    "name": "John Doe",
    "age": 25,
    "address": {
      "city": "New York",
      "country": "USA"
    }
  }
  ```

- #### 4. Update Student

  PATCH `/students/64e8f7b929b9bc3eb5f1d62b`

  ```json
  {
    "name": "John Smith"
  }
  ```

  Response:

  ```json
  {
    "message": "Student updated successfully."
  }
  ```

- #### 5. Delete Student

  DELETE `/students/64e8f7b929b9bc3eb5f1d62b`

  Response:

  ```json
  {
    "message": "Student deleted successfully."
  }
  ```

## Contributing

Feel free to fork this repository and submit pull requests for new features or bug fixes.

## License

This project is licensed under the MIT License.
