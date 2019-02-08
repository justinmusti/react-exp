import React from 'react';
import ReactDOM from 'react-dom';
import LoginUser from './LoginUser';

var element = document.getElementById('login-user');
    ReactDOM.render(<LoginUser isLoggedin={parseInt(element.getAttribute('is-user-logged-in'))} />, element);
