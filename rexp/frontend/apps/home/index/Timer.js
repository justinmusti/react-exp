import React from 'react';


class Timer extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            date: new Date()
        }
    }


    componentDidMount() {
        console.log('Component Mounted')
        this.tickerId = setInterval(()=> this.tick(), 1000)
    }


    tick(){
        this.setState({
            date: new Date()
        });
        console.log('Ticker set time', this.state.date.toLocaleTimeString())
    }

    render(){
        return (
            <div>
                <h1>Hello People</h1>
                <div>Time {this.state.date.toLocaleTimeString()}</div>
            </div>
        )

    }

    componentWillUnmount() {
        clearInterval(this.tickerId)
    }


}

export default Timer;

