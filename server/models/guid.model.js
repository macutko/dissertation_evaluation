import {model, Schema} from 'mongoose'

const schema = new Schema({
    GUID: {type: Schema.Types.String, required: true},
    grade: {type: Schema.Types.String, required: true},
});

schema.set('toJSON', {
    virtuals: true,
    versionKey: false,
    transform: function (doc, ret) {
        delete ret._id;
        delete ret.hash;
    }
});

module.exports = model('GUID', schema);