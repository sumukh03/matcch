document.addEventListener('DOMContentLoaded', function () {
    // Get references to DOM elements
    const signinPage = document.getElementById('signin-page');
    const signupPage = document.getElementById('signup-page');
    const questionnairePage = document.getElementById('questionnaire-page');
    const recommendationsPage = document.getElementById('recommendations-page');
    const recommendationButton = document.getElementById('rec-btn');
    const takeTestButton = document.getElementById('take-test-btn');
    const connectionPage = document.getElementById('connection-page');
    const signOutButton = document.getElementById('signout-btn');
    // const OPTIONS=["Strongly Agree","Agree","Neutral","Disagree","Strongly Disagree"]
    ANSWERS=[]

    const questionElement = document.getElementById("question")
    // const answerButtons = document.getElementById("answer-buttons")
    const nextButton = document.getElementById("next-button")
    const answerButtons = document.querySelectorAll('#answer-buttons .btn');

    var RETEST=false

    let currentQuestionIndex=0
    

    // Show Sign In Page by default
    showPage(signinPage);

    // Show/Hide pages
    function showPage(page) {
        const pages = document.querySelectorAll('.page');
        pages.forEach(p => p.classList.remove('show'));
        page.classList.add('show');
    }

    async function makeAPIcall(url,data){
        try {
    
            const jsonData = JSON.stringify(data)
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: jsonData,
                credentials: 'include'
            }
    
            const response = await fetch(url, options);
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const responseData = await response.json(); 
            console.log('Response from server:', responseData);
            if (responseData.status){
                return responseData
            }
            else{
                alert("ERROR OCCURED !"+responseData.message)
                window.location.reload();
            }

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            return false
        }
    
    }

    function makeRecommendations(users){
    
        users.forEach(user => {
            const userBox = document.createElement('div');
            userBox.classList.add('user-box');

            const userDetails = document.createElement('button');
            // userDetails.innerText = `Name: ${user.name},\n Gender: ${user.gender},\n<strong>Score: ${user.score}</strong>`;
            userDetails.innerHTML = `Name: ${user.name},<br> Gender: ${user.gender},<br>Score: <strong>${user.score}</strong>`;

            // userDetails.setAttribute("id","user-details")
            userBox.appendChild(userDetails);

            recommendationsPage.appendChild(userBox);


            showPage(recommendationsPage)

        })
        
    }
    async function showRecommendations(){
        //make the api call to get the recommendations 
        //add the html code 
        url="http://127.0.0.1:5000/users_end/recommendations"
        data=null
        user_recommendations = await makeAPIcall(url,data)
        if (user_recommendations.status){
            makeRecommendations(user_recommendations.data)
        }
        console.log("showRecommendatioins")
    }

    // Function to handle sign in
    async function signIn(mobile, password) {
        // Implement sign in logic here
        // Send POST request to server with username and password
        const url="http://127.0.0.1:5000/users_end/login"
        const data={"mobile":mobile,"password":password}
        console.log("SIGNIN")
        let result=await makeAPIcall(url,data)
        console.log(result)
        if (result){
            showPage(connectionPage)
            // showPage(questionnairePage)
            signOutButton.style.display="block"
            recommendationButton.onclick=showRecommendations
            takeTestButton.onclick=()=>{
                showPage(questionnairePage) 
                RETEST=true
                startTest()
            }

        }
        else {
        alert("SIGN IN FAILED , No API Response ")}
    }

    // Function to handle sign up
    async function signUp(new_user_data) {
        // Implement sign up logic here
        // Send POST request to server with new username and password
        const url="http://127.0.0.1:5000/users_end/sign_up"
        let result= await makeAPIcall(url,new_user_data)
        if (result){
            // showPage(connectionPage)
            // // showPage(questionnairePage)
            // recommendationButton.style.display="none"
            // // recommendationButton.onclick=showRecommendations
            // takeTestButton.onclick=()=>{
            //     showPage(questionnairePage) 
            //     RETEST=false
            //     startTest()
            // }

            alert("User Created, Please SIGNIN")
            document.getElementById('signup-form').reset();

        }
        else {
        alert("SIGN UP FAILED , No API Response ")}
    }



    // Event listeners for Sign In and Sign Up links
    document.getElementById('signup-link').addEventListener('click', function (e) {
        e.preventDefault();
        showPage(signupPage);
    });

    document.getElementById('signin-link').addEventListener('click', function (e) {
        e.preventDefault();
        showPage(signinPage);
    });

    // Event listener for Sign In form submission
    document.getElementById('signin-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const mobile = document.getElementById('mobile').value;
        const password = document.getElementById('password').value;
        signIn(mobile, password);
    });

    // Event listener for Sign Up form submission
    document.getElementById('signup-form').addEventListener('submit', function (e) {
        e.preventDefault();
    
        // Extracting form data
        const new_user_data = {
            name: document.getElementById('new-username').value,
            email: document.getElementById('new-email').value,
            password: document.getElementById('new-password').value,
            mobile: document.getElementById('new-mobile').value,
            city: document.getElementById('new-city').value,
            gender: document.getElementById('new-gender').value
        };
    
        // console.log(new_user_data);
    
        // Send new_user_data to signUp function or perform any other action
        signUp(new_user_data);
    });

    const QUESTIONS=[
        "I am the life of the party.",
        "I don't talk a lot.",
        "I feel comfortable around people.",
        "I keep in the background.",
        "I start conversations.",
        "I have little to say.",
        "I talk to a lot of different people at parties.",
        "I don't like to draw attention to myself.",
        "I don't mind being the center of attention.",
        "I am quiet around strangers.",
        "I get stressed out easily.",
        "I am relaxed most of the time.",
        "I worry about things.",
        "I seldom feel blue.",
        "I am easily disturbed.",
        "I get upset easily.",
        "I change my mood a lot.",
        "I have frequent mood swings.",
        "I get irritated easily.",
        "I often feel blue.",
        "I feel little concern for others.",
        "I am interested in people.",
        "I insult people.",
        "I sympathize with others' feelings.",
        "I am not interested in other people's problems.",
        "I have a soft heart.",
        "I am not really interested in others.",
        "I take time out for others.",
        "I feel others' emotions.",
        "I make people feel at ease.",
        "I am always prepared.",
        "I leave my belongings around.",
        "I pay attention to details.",
        "I make a mess of things.",
        "I get chores done right away.",
        "I often forget to put things back in their proper place.",
        "I like order.",
        "I shirk my duties.",
        "I follow a schedule.",
        "I am exacting in my work.",
        "I have a rich vocabulary.",
        "I have difficulty understanding abstract ideas.",
        "I have a vivid imagination.",
        "I am not interested in abstract ideas.",
        "I have excellent ideas.",
        "I do not have a good imagination.",
        "I am quick to understand things.",
        "I use difficult words.",
        "I spend time reflecting on things.",
        "I am full of ideas."
    ];


    function startTest(){
        currentQuestionIndex=0;
        showQuestion()
    }


    function showQuestion(){
        let currentQuestion = QUESTIONS[currentQuestionIndex]
        let questionNo = currentQuestionIndex+1
        questionElement.innerHTML=currentQuestion

        answerButtons[0].onclick=() => {
            let v=answerButtons[0].value
            console.log(v)
            ANSWERS.push(v)
            next_question()
        }

        answerButtons[1].onclick=() => {
            let v=answerButtons[1].value
            console.log(v)
            ANSWERS.push(v)
            next_question()
        }

        answerButtons[2].onclick=() => {
            let v=answerButtons[2].value
            console.log(v)
            ANSWERS.push(v)
            next_question()
        }

        answerButtons[3].onclick=() => {
            let v=answerButtons[3].value
            console.log(v)
            ANSWERS.push(v)
            next_question()
        }

        answerButtons[4].onclick=() => {
            let v=answerButtons[4].value
            console.log(v)
            ANSWERS.push(v)
            next_question()
        }
        function next_question(){
        if (currentQuestionIndex<QUESTIONS.length-1){
            currentQuestionIndex++
            showQuestion()
        }
        else{
            nextButton.style.display="block"
            nextButton.addEventListener("click",sendScore)
        }
    }
        
    }

    async function sendScore(){
        try {

            // const jsonData = JSON.stringify({"answers":ANSWERS,"retest":RETEST})
            // const url = "http://127.0.0.1:5000/process_end/test_score"
            // const options = {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json'
            //     },
            //     body: jsonData,
            //     credentials: 'include'
            // }

            // const response = await fetch(url, options);

            // if (!response.ok) {
            //     throw new Error('Network response was not ok');
            // }
            // const responseData = await response.json(); // Parse the JSON response
            // console.log('Response from server:', responseData);
            // // showPage(recommendationsPage)
            const scoreData={"answers":ANSWERS,"retest":RETEST}
            const url = "http://127.0.0.1:5000/process_end/test_score"
            responseData=await makeAPIcall(url,scoreData)

            if (responseData){
                // showRecommendations(responseData)
                showPage(connectionPage)
            // showPage(questionnairePage)
                recommendationButton.style.display="block"
                recommendationButton.onclick=showRecommendations
                takeTestButton.onclick=()=>{
                    showPage(questionnairePage) 
                    startTest()
                }
                
            }
            // Handle the response data as needed
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }

    }
    signOutButton.addEventListener('click', function () {
        // Reload the page
        window.location.reload();
        // Optionally, you can show an alert message
        // alert('You have been signed out');
    });

// startTest()
});

