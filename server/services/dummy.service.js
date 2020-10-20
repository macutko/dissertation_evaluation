import {Dummy} from '../models/db'
import bcrypt from "bcryptjs";
import {config} from '../config/config'

module.exports = {
    create,
    get,
    removeObject,
    update
};

async function create(request) {
    console.log(request)
    if (!request.title) throw 'No title'
    if (!request.text) throw 'No text'
    const dummy = new Dummy(request);

    await dummy.save()
    return dummy.toJSON()
}

async function removeObject({email, password}) {
    const user = await Dummy.findOne({email});
    if (user && bcrypt.compareSync(password, user.hash)) {
        const token = jwt.sign({sub: user.id}, config.secret);
        return [user.toJSON(), token]
    }
}

async function update(userID, params) {
    const user = await Dummy.findById(userID);
    if (!user) throw 'User not found'
    if (params.password === undefined) throw 'Password must be defined'

    user.hash = bcrypt.hashSync(params.password, 10);

    // save agent
    let r = undefined;
    await user.save().then((agent) => {

        r = {
            ...agent.toJSON(),
        };

    });
    return user.toJSON()
}

async function get(id) {
    return await Dummy.findById(id);
}



