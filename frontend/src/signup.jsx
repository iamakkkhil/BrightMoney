import React, { useState } from "react";
import "./css/main.css";

var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

export default function Signup() {
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [isSuccessful, setIsSuccessful] = useState(true);

    const handleSubmit = (event) => {
        event.preventDefault();
        var { email, uname, lname, pass } = document.forms[0];

        if (email.value && uname.value && lname.value && pass.value) {
            // TODO: add user to database via API call
            setIsSubmitted(true);
        }
        

        var raw = JSON.stringify({
            "email": email.value,
            "first_name": uname.value,
            "last_name": lname.value,
            "password": pass.value
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch("http://127.0.0.1:8000/accounts/api/signup", requestOptions)
            .then((response) => {
                if(!response.ok){ 
                    setIsSuccessful(false);
                    throw new Error(response.status)
                }
                else return response.json()
            })
            .then((result) => {
                setIsSuccessful(true)
            })
            .catch(error => {
                console.log('error', error)
                setIsSuccessful(false);
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
              <label>First Name </label>
              <input type="text" name="uname" required />
            </div>
            <div className="input-container">
              <label>Last Name </label>
              <input type="text" name="lname" required />
            </div>
            <div className="input-container">
              <label>Password </label>
              <input type="password" name="pass" required />
            </div>
            <div className="button-container">
              <input type="submit" />
            </div>
          </form>
          {
            isSuccessful ? null : <div className="error">Email already exists</div> 
          }
        </div>
      );

    return (
        <div className="app">
            <div className="auth-form">
                <div className="title">Sign up</div>
                {isSubmitted && isSuccessful ? 
                    <div>
                        User successfully registered!
                        <div>
                        <a href="/login">Back to Login</a>
                        </div>
                    </div>
                 : renderForm}
            </div>
        </div>
    );
}