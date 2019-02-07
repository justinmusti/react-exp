import React from 'react';

export default class LoginUser extends React.Component{

    constructor(props){
        super(props);
        console.log('PROPS', props);
        let isLoggedin = false;
        if (props.hasOwnProperty('isLoggedin')){
            isLoggedin = props.isLoggedin;
        }

        this.state = {
            isLoggedin: isLoggedin,
        }
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
            <form action="" className="ui form">
                <div className="field">
                    <input type="text" name={'username'} placeholder={'Username'}/>
                </div>
                <div className="field">
                    <input type="password" name={'password'}  placeholder={'Password'}/>
                </div>
                <button className="ui primary button">Login</button>
            </form>
        )

    }

}