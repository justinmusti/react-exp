import React from 'react';


export default class RegisterUser extends React.Component{
    constructor(props){
        super(props);
        console.log(props);

        this.handleUsername = this.handleUsername.bind(this);
        this.handlePassword = this.handlePassword.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        this.state = {
            isLoggedin: props.isLoggedin| false,
            isProcessing: false,
            error: '',
            registerUrl: props.registerUrl,
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
        //Stop form from being processed/submitted.
        event.preventDefault();

        //Validate form fields before submit
        if(!this.state.data.username){
            this.setState({error: 'Username cannot be empty.'});
            return;
        }
        if (!this.state.data.password) {
            this.setState({error: 'Password cannot be empty.'});
            return;
        }
        this.setState({isProcessing: true});
        //Submit the form to endpoint
        fetch(this.state.registerUrl,
            {
                method: "POST",
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify(this.state.data)
            })
            .then(response => response.json()).then(response=>{

                    if(!response.status){
                        this.setState({isProcessing: false})
                        this.setState({error: response.error});
                        return;
                    }
                    window.location.href = '/'
        }).catch(response => {
            this.setState({
                error: 'Something went wrong. Please try again later.',
                isProcessing: false
            })
        })

        console.log('Form Submitted');
    }

    getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }


    render(){

        if(this.state.isLoggedin){
            return(
                <div className="ui warning message">
                    <p>There seems to be an online session at the moment.
                        <br/>
                        Please logout to be able to register.
                    </p>
                </div>
            )
        }

        return(
            <div>
                {this.state.error && <div className="ui error message">
                    <p>{this.state.error}</p>
                </div>}
                <form className={"ui "+ (this.state.isProcessing? ' loading ':'') +" form"} onSubmit={this.handleSubmit}>
                    <div className="field">
                        <input type="text" name={'username'} defaultValue={this.state.data.username}
                            placeholder={'Username'}
                            onChange={this.handleUsername}/>
                    </div>
                    <div className="field">
                        <input type="password" name={'password'} defaultValue={this.state.data.password}
                               placeholder={'Password'}
                               onChange={this.handlePassword}/>
                    </div>
                    <button className="ui primary button" onClick={this.handleSubmit}>Register</button>
                </form>
            </div>
        )
    }


}