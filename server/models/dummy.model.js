import {Schema, model} from 'mongoose'

const schema = new Schema({
    title: {type: String, required: true},
    text: {type: String, required: true},
});

schema.set('toJSON', {
    virtuals: true,
    versionKey: false,
    transform: function (doc, ret) {
        delete ret._id;
        delete ret.hash;
    }
});

module.exports = model('Dummy', schema);