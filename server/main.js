import 'rootpath'

import express from 'express'

const app = express();
import cors from 'cors'
import bodyParser from 'body-parser'
import {createServer} from "http"

import {config} from './config/config.js'


app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());
app.use(cors());


// api routes
app.use('/', require('./api/controllers/dummy.controller'));

// start server
const port = process.env.NODE_ENV === 'production' ? (process.env.PORT || 8080) : (config.PORT || 4000);
const server = createServer(app);

server.listen(port, () => console.log("server running on port:" + port));