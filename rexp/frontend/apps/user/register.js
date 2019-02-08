import React from 'react';
import ReactDOM from 'react-dom';
import RegisterUser from './RegisterUser';

var element = document.getElementById('register-user');
    ReactDOM.render(<RegisterUser
        isLoggedin={parseInt(element.getAttribute('is-user-logged-in'))} registerUrl={element.getAttribute('user-register-url')} />, element);
