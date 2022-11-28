import React, { useState } from "react";
import "./css/main.css";

var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");


export default function Login() {
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [isSuccessful, setIsSuccessful] = useState(true);

    const handleSubmit = (event) => {
        event.preventDefault();

        var { email, pass } = document.forms[0];
        
        var raw = JSON.stringify({
            "email": email.value,
            "password": pass.value
        });
        
        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };
        
        fetch("http://127.0.0.1:8000/accounts/api/login", requestOptions)
            .then(response => {
                if(!response.ok){ 
                    setIsSuccessful(false);
                    throw new Error(response.status)
                }
                else return response.json()
            })
            .then((result) => {
                localStorage.setItem('access_token', result.access_token)
                localStorage.setItem('refresh_token', result.refresh_token)
                setIsSubmitted(true)
                setIsSuccessful(true)
            })
            .catch(error => {
                console.log('error', error)
                setIsSuccessful(false)
            });

    };

    const renderForm = (
        <div className="form">
            <form onSubmit={handleSubmit}>
                <div className="input-container">
                    <label>Email </label>
                    <input type="text" name="email" required />
                    
                </div>
                <div className="input-container">
                    <label>Password </label>
                    <input type="password" name="pass" required />
                    
                </div>
                <div className="button-container">
                    <input type="submit" />
                </div>
                <div className="info"><a href="/signup">Don't have a account? Sign Up</a></div> 
            </form>
            {
            isSuccessful ? null : <div className="error">Invalid Credentials</div> 
          }
        </div>
    );

    return (
        <div className="app">
            <div className="auth-form">
                <div className="title">Login</div>
                {isSubmitted ? 
                    <div>
                        User is successfully logged in
                        <br />
                        <a href="/">Back to Home</a>
                    </div>

                : renderForm}
            </div>
        </div>
    );
}