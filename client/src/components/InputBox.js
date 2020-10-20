import React from "react";
import './styles/OutPut.css';
import {InputGroup, Input} from "reactstrap";
import './styles/InputBox.css';

export default class OutPut extends React.Component {

    render() {
        return (
            <>
                <InputGroup>
                    <Input id={"title"} placeholder={"title"} className={'inputContainer'} onChange={this.props.input}
                           type="textarea"/>
                </InputGroup>

                <InputGroup>
                    <Input id={"text"} placeholder={"text"} className={'inputContainer'} onChange={this.props.input}
                           type="textarea"/>
                </InputGroup>
            </>
        )
    }
}