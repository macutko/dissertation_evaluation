import {config} from "../config/config";
import mongoose from 'mongoose'

const connectionOptions = {
    useCreateIndex: true,
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false
};
mongoose.connect(process.env.MONGODB_URI || config.connectionString, connectionOptions);
mongoose.Promise = global.Promise;

module.exports = {

    GUID: require('./guid.model'),
    Subject: require('./subject.model'),

};
