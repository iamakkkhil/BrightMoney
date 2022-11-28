import { useState, useEffect } from 'react'
import { Navigate } from "react-router-dom";
import './App.css'
import PlaidOuth from './plaidoauth';

// let navigate = useNavigate();

const updateAccessToken = () => {
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");
  myHeaders.append("Authorization", "Bearer " + localStorage.getItem("access_token"));

  var raw = JSON.stringify({
    "refresh_token": localStorage.getItem("refresh_token")
  });

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };

  fetch("http://127.0.0.1:8000/accounts/api/token/refresh/", requestOptions)
    .then(response => {
      if(!response.ok){ 
        throw new Error(response.status)
      }
      else return response.json()
    })
    .then(result => {
      localStorage.setItem('access_token', result.token)
      console.log("Access token updated successfully");
    })
    .catch(error => console.log('error', error));
}


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true);

  useEffect(() => {
    const access_token = localStorage.getItem("access_token");
    const refresh_token = localStorage.getItem("refresh_token");

    if (!(access_token) || !(refresh_token)) {
      console.log("No access token or refresh token found");
      setIsLoggedIn(false)
    }
  }, []);

  return (
    <div>

      {isLoggedIn ? <PlaidOuth />: 
      <Navigate to="/login" />}
    </div>
  )
}

export default App
