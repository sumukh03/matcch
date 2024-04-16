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
 
   <img width="547"  src="https://github.com/sumukh03/matcch/assets/126386392/71764fb7-d7f8-44bd-a80d-909290f54853">

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

After the server starts,
go to 

```bash
http://localhost:3000/
```
on your browser 

## Technical Details

#### Introduction

+ According to the compatibility data mentioned , similar users are more compatible with eachother.

  <img width="985" src="https://github.com/sumukh03/matcch/assets/126386392/949d31fa-4615-409c-9cbd-8be6cccbe61f">
+ Hence, to find the compatible users , we first find the cluster that the user belongs to.
+ Then , inside the cluster , we find the similar vectors using the distance between them.
+ This distance determines the closest vectors.
+ To the closest vectors , we find the compatibility points.

#### Kmeans Clustering

+ The raw data from the dataset is filtered to form the score vector of order [ O , C , E , A , N ].
+ These vectors are then fitted to the Kmeans model consisting four clusters.
+ The optimum number of centroids are calculated using Elbow method with WCSS (with-in-cluster sum of squares) parameter.
  
  <img width="413"  src="https://github.com/sumukh03/matcch/assets/126386392/9a7e7b29-b3f3-4bf4-aeb2-527f1b1c3c35">

#### Categorising the new vector

+ When we have the new user_score vector , firstly , we try to find the cluster to which the vector belongs
+ From the cluster , we use the linear distance to find nearest similar neighbour vectors to the new user_score vector.

#### The Compatibility Factor

+ Now that we have the similar vectors to the given user vector
+ We assign the Compatibility points to each of the similar vectors with respect to the new user vector from the compatibility data.

#### Database
+ The database is initialised with the training data of 5000 users for simplicity.
+ When the new user takes the test , the score is store on the database.
+ When the new user's count reaches a threshold , we can use that data and retrain our model.

### Documentation
Kindly find the manual about how to use the application and the API's in the folder
```bash
matcch/Docs 
```
### Sample output 
Here is a quick look of the result.  
For the given user score vector , the user with user_id 505 is the most compatible user with the corresponding compatible points.  

  <img width="842" src="https://github.com/sumukh03/matcch/assets/126386392/b996965a-633b-4abc-bcb1-f052eb4fa73c">


## Example Use Cases 
1. Dating or matrimonial systems that can recommend a set of users from the database to a particular user.
2. For content based filtering systems , similar compatible users can be recommended simialar content.
