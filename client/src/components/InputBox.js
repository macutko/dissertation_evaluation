import React from "react";
import './styles/OutPut.css';
import {InputGroup, Input} from "reactstrap";
import './styles/InputBox.css';

export default class OutPut extends React.Component {

    render() {
        return (
            <>
                <InputGroup>
                    <Input id={"GUID"} placeholder={"GUID"} className={'inputContainer'} onChange={this.props.input}
                           type="textarea"/>
                </InputGroup>

                <InputGroup>
                    <Input id={"subject"} placeholder={"subject"} className={'inputContainer'} onChange={this.props.input}
                           type="textarea"/>
                </InputGroup>

                <InputGroup>
                    <Input id={"grade"} placeholder={"grade"} className={'inputContainer'} onChange={this.props.input}
                           type="textarea"/>
                </InputGroup>
            </>
        )
    }
}