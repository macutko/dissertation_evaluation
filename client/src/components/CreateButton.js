import React from "react";
import axiosInstance from "./axiosInstance";
import Button from "react-bootstrap";

export default class CreateButton extends React.Component {
    handleClick = () => {
        axiosInstance
            .post("/create", {
                text: this.props.text,
                title: this.props.title
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