import {GUID} from '../models/db'

module.exports = {
    create,
    get,
    remove,
    update
};

async function create(request) {
    let time = 0;
    if (!request.GUID) throw 'No GUID'
    if (!request.grade) throw 'No grade'
    const dummy = new GUID(request);

    await dummy.save()
    return {...dummy.toJSON(), time: time}
}


async function update(req) {
    if (!req.GUID) throw 'No GUID'
    if (!req.grade) throw 'No grade'

    const user = await GUID.findOne({GUID: req.GUID});
    if (!user) throw 'User not found'

    user.grade = req.grade

    await user.save()


    return user.toJSON()
}

async function get(req) {
    if (req.GUID) {
        return await GUID.find({GUID: req.GUID});
    } else if (req.grade) {
        return await GUID.find({grade: req.grade})
    } else throw 'No params!'
}


async function remove(req) {
    return GUID.findOneAndRemove({GUID: req.GUID});
}




