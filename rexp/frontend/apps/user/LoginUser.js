import React from 'react';
import {getCookie} from '../utils';

export default class LoginUser extends React.Component{

    constructor(props){
        super(props);
        let isLoggedin = false;
        if (props.hasOwnProperty('isLoggedin')){
            isLoggedin = props.isLoggedin;
        }
        this.handleUsername = this.handleUsername.bind(this);
        this.handlePassword = this.handlePassword.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.state = {
            isLoggedin: isLoggedin,
            isProcessing: false,
            error: '',
            data: {
                username: '',
                password: '',
            }
        }
    }

    handleUsername(event){
        let data = this.state.data;
        data.username = event.target.value;
        this.setState({data:data})
    }

    handlePassword(event) {
        let data = this.state.data;
        data.password = event.target.value;
        this.setState({data: data})
    }

    handleSubmit(event){
        //validate username and password first
        if (!this.state.data.username || this.state.data.username.length < 4){
            this.setState({error: 'Username must be at least 4 characters'});
            return;
        }
        if (!this.state.data.password || this.state.data.password.length < 6) {
            this.setState({error: 'Password must be at least 6 characters'});
            return;
        }



        this.setState({isProcessing: true});
        fetch('/user/login-do/',
            {
                method: "POST",
                credentials: 'include',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                body: JSON.stringify(this.state.data)
            })
            .then(response=>response.json())
            .then(response =>{
                this.setState({isProcessing: false});
                if (!response.status){
                    this.setState({error: response.error});
                    return;
                }
                window.location.href = '/';
            });
        event.preventDefault();
    }

    render(){
        if(this.state.isLoggedin){
            return(
                <div className="ui positive message">
                    <p>
                        You are already logged in.
                    </p>
                </div>
            )
        }

        return(
            <div>
                {this.state.error && <div className="ui error message">
                    <p>{this.state.error}</p>
                </div>}
                <form action="javascript:viod(0);"
                      className={"ui " + (this.state.isProcessing ? " loading " : "") + " form"}
                      onSubmit={this.handleSubmit}>
                    <div className="field">
                        <input type="text" name={'username'} placeholder={'Username'}
                               defaultValue={this.state.data.username}
                               onChange={this.handleUsername}/>
                    </div>
                    <div className="field">
                        <input type="password" name={'password'} placeholder={'Password'}
                               defaultValue={this.state.data.password}
                               onChange={this.handlePassword}/>
                    </div>
                    <button className="ui primary button" onClick={this.handleSubmit}>Login</button>
                </form>
            </div>

        )

    }

}