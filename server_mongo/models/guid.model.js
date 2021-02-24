import {model, Schema} from 'mongoose'

const schema = new Schema({
    GUID: {type: Schema.Types.String, required: true, unique: true, dropDups: true},
    subjects: [{type: Schema.Types.ObjectID, ref: 'Subject'}]
});

schema.set('toJSON', {
    virtuals: true,
    versionKey: false,
    transform: function (doc, ret) {
        delete ret._id;
    }
});

module.exports = model('GUID', schema);
