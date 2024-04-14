import React, { useState } from 'react';
import RecommendationsPage from './RecommendationsPage'
const QUESTIONS = [
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

const OPTIONS = [
  { id: 1, text: 'Strongly Agree', points: 5,styleId:"Strongly" },
  { id: 2, text: 'Agree', points: 4 ,styleId:"Agree"},
  { id: 3, text: 'Neutral', points: 3 ,styleId:"Neutral"},
  { id: 4, text: 'Disagree', points: 2,styleId:"Disagree" },
  { id: 5, text: 'Strongly Disagree', points: 1,styleId:"StronglyDis" }
];

const QuestionsPage = () => {
  const [mobile, setMobileNumber] = useState('');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [recommendations, setRecommendations] = useState([]);
  const [showQuestions, setShowQuestions] = useState(false);
  const [user_id, setUserID] = useState('');
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [showSubmit,setShowSubmit]=useState(false)


  const handleMobileNumberChange = (event) => {
    setMobileNumber(event.target.value);
  };


  const handleOptionSelect = (option) => {
    const currentQuestionId = currentQuestionIndex;
    setAnswers({ ...answers, [currentQuestionId]: option.points });
    if (currentQuestionIndex < QUESTIONS.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      setShowQuestions(false);
      setShowSubmit(true)
    }
  };


  async function makeAPIcall(url, data) {
    try {
        console.log(data)
      const jsonData = JSON.stringify(data);
      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: jsonData
      };

      const response = await fetch(url, options);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const responseData = await response.json();
      return responseData;

    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      alert("ERROR Try again");
      window.location.reload();
      return { status: false, message: 'Error occurred during API call' };
    }
  }

  const handleMobileNumberSubmit = async () => {
    try {
      const response = await makeAPIcall('http://127.0.0.1:5000/users_end/details', { mobile });
      if (response.status) {
        setUserID(response.data);
        setShowQuestions(true);
      } else {
        console.error('Error:', response.message);
      }
    } catch (error) {
      console.error('Error submitting mobile number:', error);
    }
  };

  const handleSubmit = async () => {
    try {
        let answer_data={
            "user_id":user_id,
            "answers":Object.values(answers)
        }
      const response = await makeAPIcall('http://127.0.0.1:5000/process_end/test_score',  answer_data);

      if (response.status) {
        setRecommendations(response.data);
        setShowRecommendations(true)
        setShowSubmit(false)
      } else {
        console.error('Error:', response.message);
      }
    } catch (error) {
      console.error('Error submitting answers:', error);
    }
  };

  return (
    <div>
      <h1 id='Matcch'>Matcch</h1>
      {!showQuestions && !showSubmit && !showRecommendations  && (
        <div>
          <h3>Find people</h3>
          <label htmlFor="mobileNumber"><p>Enter mobile number and find people like you </p></label>
          <input
            type="text"
            id="mobileNumber"
            value={mobile}
            onChange={handleMobileNumberChange}
            placeholder='Mobile'
          />
          <button className ='SubmitButton' onClick={handleMobileNumberSubmit}>Submit</button>
        </div>
      )}
      {showQuestions && (
        <div>
          <p>Answer these questions</p>
          <h2 className='questions'>{QUESTIONS[currentQuestionIndex]}</h2>
          {OPTIONS.map((option) => (
            <button className='options' id={option.styleId}
              key={option.id}
              onClick={() => handleOptionSelect(option)}
            >
              {option.text}
            </button>
          ))}
        </div>
      )}
      {showSubmit&&(
        <div>
        <p>Thankyou! for answering</p>
        <h3>Click to find users like you !!</h3>
      <button className ='SubmitButton' onClick={handleSubmit}>Find People</button>
      </div>
      )}
      {showRecommendations && 
        <div>
          <h2>Compatible Users</h2>
          <RecommendationsPage
            data={recommendations}
          />
          
        </div>
      }
    </div>
  );
}

export default QuestionsPage;

