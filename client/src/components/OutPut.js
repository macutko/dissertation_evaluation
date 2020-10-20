import React from "react";
import './styles/OutPut.css';


export default class OutPut extends React.Component {

    render() {
        return (

            <div className={'textContainer'}>
                {
                    this.props.text === "{}" ?
                        <p className={'color'}>{this.props.text}</p> :
                        <p className={'noColor'}>{this.props.text}</p>
                }
            </div>

        )
    }
}