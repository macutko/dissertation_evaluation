import {model, Schema} from 'mongoose'

const schema = new Schema({
    GUID: {type: Schema.Types.String, required: true},
    grades: [{
        subject: Schema.Types.String,
        grade: Schema.Types.String,
    }]
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