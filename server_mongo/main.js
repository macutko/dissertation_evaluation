import 'rootpath'

import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
import {createServer} from "http"

import {config} from './config/config.js'

const app = express();

//to decode the body of the request
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

//for clients to work
app.use(cors());


// api routes
app.use('/', require('./api/example.controller'));

// start server
const port = process.env.NODE_ENV === 'production' ? (process.env.PORT || 8080) : (config.PORT || 4000);
const server = createServer(app);

server.listen(port, () => console.log("server running on port:" + port));
