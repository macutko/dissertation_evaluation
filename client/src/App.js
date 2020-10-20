import React from "react";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import HomePage from "./pages/HomePage";



// TODO: double check the cookie tutorial for CSRF hacks
export default class App extends React.Component {


    render() {
        return (
            <Router>
                <div className="body-element">
                    <Switch>
                        <Route exact path="/" component={HomePage}/>
                    </Switch>
                </div>
            </Router>
        );
    }
}
