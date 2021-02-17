import React from "react";
import OutPut from "../components/OutPut";
import InputBox from "../components/InputBox";
import {Container, Row} from "react-bootstrap";
import CreateButton from "../components/CreateButton";
import GetButton from "../components/GetButton";
import UpdateButton from "../components/UpdateButton";

export default class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            response: 'response',
            GUID: "",
            subject: "",
            grade: ""
        }
    }

    changeInput = (event) => {
        this.setState({
            [event.target.id]: event.target.value
        })
    }
    updateOutput = (text) => {
        this.setState({response: text})
    }

    render() {
        return (
            <div style={{backgroundColor: "#a20909", minHeight: '100vh'}}>

                <Container>

                    <Row>
                        <InputBox input={this.changeInput}/>
                    </Row>
                    <Row style={{marginTop: "10px"}}>
                        <CreateButton GUID={this.state.GUID} grade={this.state.grade} subject={this.state.subject}
                                      updateOutput={this.updateOutput}
                                      className={'col-sm'}/>
                        <UpdateButton GUID={this.state.GUID} grade={this.state.grade} subject={this.state.subject}
                                      updateOutput={this.updateOutput}
                                      className={'col-sm'}/>
                        <GetButton GUID={this.state.GUID} grade={this.state.grade} updateOutput={this.updateOutput}
                                   subject={this.state.subject}
                                   className={'col-sm'}/>
                    </Row>

                    <Row>
                        <OutPut text={this.state.response}/>
                    </Row>
                </Container>
            </div>
        );
    }
}
