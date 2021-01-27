import React from "react";
import axiosInstance from "./axiosInstance";
import {Button} from "react-bootstrap";

export default class DeleteButton extends React.Component {
    handleClick = () => {
        axiosInstance
            .delete("/delete", {
                params: {
                    GUID: this.props.GUID
                }
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
                    Delete
                </Button>
            </div>
        )
    }
}