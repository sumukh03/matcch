

---

# matcch

## Description
This project consists of a frontend and a backend component, both running in separate Docker containers. The frontend is built with React, while the backend is built with Flask.

## Installation and Usage

### Frontend Setup
1. Navigate to the Frontend directory:
    ```
    cd Frontend
    ```
2. Build the Docker image for the React app:
    ```
    docker build -t react-app .
    ```
3. Run the Docker container for the React app:
    ```
    docker run react-app
    ```

### Backend Setup
1. Navigate to the Backend directory:
    ```
    cd Backend
    ```
2. Build the Docker image for the Flask app:
    ```
    docker build -t flask-app .
    ```
3. Run the Docker container for the Flask app:
    ```
    docker run flask-app
    ```

### Running All Containers
To run all the containers together, from the main directory (i.e., `matcch`), run:
```
docker compose up --build
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

---

Feel free to modify it according to your project's specific details and needs!
