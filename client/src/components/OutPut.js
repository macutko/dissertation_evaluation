import React from "react";
import './styles/OutPut.css';


export default class OutPut extends React.Component {

    render() {
        return (
            <div className={'textContainer'}>
                <p className={'color'}>Status: {this.props.text.status ? JSON.stringify(this.props.text.status) : null}</p>
                <p className={'color'}>Response: {this.props.text.data ? JSON.stringify(this.props.text.data) : null}</p>
                {this.props.text.data ?
                    <p className={'color'}>Time: {this.props.text.data.time}</p>
                    : null}

            </div>

        )
    }
}