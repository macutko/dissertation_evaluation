import React from "react";
import {Link} from "react-router-dom";
import {Navbar, Nav} from "react-bootstrap";

export default class NavBarMenu extends React.Component {
    render() {
        return (
            <Navbar sticky="top" bg="dark" variant="dark">
                <Navbar.Brand>Dummy Crud Client</Navbar.Brand>
                <Nav className="ml-auto">
                    <Nav.Link as={Link} to="/">
                        CRUD
                    </Nav.Link>
                </Nav>
            </Navbar>
        );
    }
}
