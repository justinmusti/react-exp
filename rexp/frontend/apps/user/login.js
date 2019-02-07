import React from 'react';
import ReactDOM from 'react-dom';
import LoginUser from './LoginUser';


ReactDOM.render(<LoginUser isLoggedin={true} />, document.getElementById('login-user'));