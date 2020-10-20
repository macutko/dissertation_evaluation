import React from "react";
import NavBarMenu from "../components/NavBarMenu";
import OutPut from "../components/OutPut";
import InputBox from "../components/InputBox";
import {Container, Row} from "react-bootstrap";
import CreateButton from "../components/CreateButton";

export default class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            outputText: "{  }",
            title: "",
            text: ""
        }
    }

    changeInput = (event) => {
        console.log(event.target.value)
        this.setState({
                [event.target.id]: event.target.value
            },
            () => console.log(this.state)
        )
    }
    updateOutput = (text) => {
        this.setState({outputText: JSON.stringify(text)})
    }

    render() {
        return (
            <div style={{backgroundColor: "#a20909", minHeight: '100vh'}}>
                <NavBarMenu/>
                <Container>
                    <Row>
                        <OutPut text={this.state.outputText}/>
                    </Row>
                    <Row>
                        <InputBox input={this.changeInput}/>
                    </Row>
                    <Row style={{marginTop: "10px"}}>
                        <CreateButton title={this.state.title} text={this.state.text} updateOutput={this.updateOutput}
                                      className={'col-sm'}/>
                    </Row>
                </Container>
            </div>
        );
    }
}
