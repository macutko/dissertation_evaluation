import React from "react";
import axiosInstance from "./axiosInstance";
import {Button} from "react-bootstrap";

export default class UpdateButton extends React.Component {
    handleClick = () => {
        axiosInstance
            .put("/update", {
                GUID: this.props.GUID,
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
                    Update
                </Button>
            </div>
        )
    }
}