after cloning 
to start the Frontend container , run the commands:
  cd Frontend/
  docker build -t react-app .
  docker run react-app

to start the Backend container , run the commands :
  cd Backend/
  docker build -t flask-app .
  docker run flask-app


to run all the containers, from the main (i.e. matcch) directory , run :
  docker compose up --build 
  
