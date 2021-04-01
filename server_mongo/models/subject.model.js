import {model, Schema} from 'mongoose'

// a subject record with a grade attached to it
const schema = new Schema({
    subjectName: {type: Schema.Types.String, required: true},
    grade: {type: Schema.Types.String, required: true},
});

schema.set('toJSON', {
    virtuals: true,
    versionKey: false,
    transform: function (doc, ret) {
        delete ret._id;
    }
});

module.exports = model('Subject', schema);
