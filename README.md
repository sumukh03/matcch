
# Matcch

Matcch is a __USER RECOMMENDATION__ system that works on the __PERSONALITY__ of the user.  
It is totally based on the Big5 personality traits of the user.  
In this we evaluate the user for their traits.  

They are:  
&nbsp;&nbsp;&nbsp;&nbsp;1 : O - Openness.  
&nbsp;&nbsp;&nbsp;&nbsp;2 : C - Conscientiousness.  
&nbsp;&nbsp;&nbsp;&nbsp;3 : E - Extraversion.  
&nbsp;&nbsp;&nbsp;&nbsp;4 : A - Agreeableness.  
&nbsp;&nbsp;&nbsp;&nbsp;5 : N - Neuroticism.  
also known as OCEAN traits.  

### STEPS 
1. The user takes a __personality test__ which gives the personality score of the user.   
2. Based on the score, user is categorised into one of the __four clusters__.  
3. There after we use the Euclidean distance to find the nearest user personalities in the cluster.













## Datasets

 - [Training data for Big5 personality traits](https://www.kaggle.com/datasets/tunguz/big-five-personality-test)
 - [Compatibility data (raw format)](https://www.typematchapp.com/who-should-you-date-based-on-your-big-5-personality-results/)



## Run Locally

Clone the project

```bash
  git clone https://github.com/sumukh03/matcch.git
```

Go to the project directory

```bash
  cd matcch
```

Install the Docker and DockerCompose and run 

```bash
docker compose up --build
```

After the server starts   
On the browser , Open 
```bash
http://localhost:3000/
```

