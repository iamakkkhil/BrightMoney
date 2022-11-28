import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import "./css/main.css";

export default function Logout() {
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  
  useEffect(() => {
    const access_token = localStorage.getItem("access_token");
    const refresh_token = localStorage.getItem("refresh_token");

    if (!access_token || !refresh_token) {
      console.log("No access token or refresh token found");
      setIsLoggedIn(false);
    }
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    var myHeaders = new Headers();
    myHeaders.append(
      "Authorization",
      "Bearer " + localStorage.getItem("access_token")
    );

    var requestOptions = {
      method: "POST",
      headers: myHeaders,
      redirect: "follow",
    };

    fetch("http://127.0.0.1:8000/accounts/api/logout", requestOptions)
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        localStorage.clear();
        setIsLoggedIn(false);
      })
      .catch((error) => console.log("error", error));
  };

  return (
    <div>
      {isLoggedIn ? (
        <div className="app">
          <div className="auth-form">
            <div className="title">Logout</div>
            <form onSubmit={handleSubmit}>
              {setIsLoggedIn ? (
                <div className="button-container">
                  <input type="submit" value="Logout" />
                  <br />
                </div>
              ) : 
              <div>
                Logged out successfully <br/>
                <a href="/login">Back to Login</a>
                </div>}
            </form>
          </div>
        </div>
      ) : (
        <Navigate to="/login" />
      )}
    </div>
  );
}
