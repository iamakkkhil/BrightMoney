import React, { useState } from "react";
import { PlaidLink } from "react-plaid-link";

// var perf = require('./plaidLink.html');

import {
  usePlaidLink,
  //   // PlaidLinkOptions,
  //   // PlaidLinkOnSuccess,
} from "react-plaid-link";

import "./css/main.css";

export default function PlaidOuth() {
  // const [isSubmitted, setIsSubmitted] = useState(false);
  const [sSuccessful, setIsSuccessful] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [tokenFetched, setTokenFetched] = useState(false);
  const [linkToken, setLinkToken] = useState("");

  // let linkToken = null;

  function getLinkToken() {
    var myHeaders = new Headers();
    myHeaders.append(
      "Authorization",
      "Bearer " + localStorage.getItem("access_token")
    );

    var requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow",
    };

    fetch(
      "http://127.0.0.1:8000/plaid/api/oauth/getPublicToken",
      requestOptions
    )
      .then((response) => {
        if (!response.ok) {
          setIsSuccessful(false);
          throw new Error(response.status);
        } else return response.json();
      })
      .then((result) => {
        setLinkToken(result.link_token);
        setTokenFetched(true);
        setIsSuccessful(true);
      })
      .catch((error) => console.log("error", error));
  }

  // function connectAccount(link_token) {
  const { open, exit, ready } = usePlaidLink({
    onSuccess: (public_token, metadata) => {
      // send public_token to server
      var myHeaders = new Headers();
      myHeaders.append(
        "Authorization",
        "Bearer " + localStorage.getItem("access_token")
      );
      myHeaders.append("Content-Type", "application/json");

      var raw = JSON.stringify({
        token: `${public_token}`,
      });

      var requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow",
      };

      fetch(
        "http://127.0.0.1:8000/plaid/api/oauth/generateAccessToken",
        requestOptions
      )
        .then((response) => response.json())
        .then((result) => console.log(result))
        .catch((error) => console.log("error", error));
      
    },

    onExit: (err, metadata) => {
      console.log("onExit", err, metadata);
    },
    onEvent: (eventName, metadata) => {
      console.log("onEvent", eventName, metadata);
    },
    token: `${linkToken}`,
    //required for OAuth; if not using OAuth, set to null or omit:
    // receivedRedirectUri: window.location.href,
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    setIsLoading(true);
    getLinkToken();
    // connectAccount(linkToken);
  };

  return (
    <div>
      <h1>Plaid Oauth</h1>
      <div className="form">
        <form onSubmit={handleSubmit}>
          {isLoading ? (
            <div>Loading</div>
          ) : (
            <div className="button-container">
              <input type="submit" value="Link Plaid" />
              <br />
            </div>
          )}
        </form>

        {tokenFetched ? (
          <button onClick={() => open()} disabled={!ready}>
            Connect a bank account
          </button>
        ) : null}

        <br />
        <div>
          <h3><a href="/logout">Logout</a></h3>
        </div>
      </div>
    </div>
  );
}
