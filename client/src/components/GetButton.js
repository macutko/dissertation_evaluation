import React from "react";
import axiosInstance from "./axiosInstance";
import {Button} from "react-bootstrap";

export default class GetButton extends React.Component {
    handleClick = () => {
        if (this.props.GUID) {
            axiosInstance
                .get("/get", {
                    params: {
                        GUID: this.props.GUID,
                    }
                })
                .then((response) => {
                    this.props.updateOutput(response)
                })
                .catch((error) => {
                    this.props.updateOutput(error)
                });
        } else if (this.props.grade) {

            axiosInstance
                .get("/get", {
                    params: {
                        grade: this.props.grade,
                    }
                })
                .then((response) => {
                    this.props.updateOutput(response)
                })
                .catch((error) => {
                    this.props.updateOutput(error)
                });
        } else if (this.props.subject) {
            axiosInstance
                .get("/get", {
                    params: {
                        subject: this.props.subject,
                    }
                })
                .then((response) => {
                    this.props.updateOutput(response)
                })
                .catch((error) => {
                    this.props.updateOutput(error)
                });
        }
    }

    render() {
        return (
            <div className={this.props.className}>
                <Button onClick={this.handleClick}>
                    Get
                </Button>
            </div>
        )
    }
}
