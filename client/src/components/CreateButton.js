import React from "react";
import axiosInstance from "./axiosInstance";
import {Button} from "react-bootstrap";

export default class CreateButton extends React.Component {
    handleClick = () => {
        axiosInstance
            .post("/create", {
                GUID: this.props.GUID,
                subject: this.props.subject,
                grade: this.props.grade
            })
            .then((response) => {
                this.props.updateOutput(response)
            })
            .catch((error) => {
                this.props.updateOutput(error)
            });
    }

    render() {
        return (
            <div className={this.props.className}>
                <Button onClick={this.handleClick}>
                    Create
                </Button>
            </div>
        )
    }
}