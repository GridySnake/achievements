import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import {AuthWrapper} from "./hooks/AuthHooks";
import {BrowserRouter} from "react-router-dom";

ReactDOM.render(
    <BrowserRouter>
        <AuthWrapper>
            <App />
        </AuthWrapper>
        </BrowserRouter>,
  document.getElementById('root')
);
