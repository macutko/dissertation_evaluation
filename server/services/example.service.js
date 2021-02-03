import {GUID} from '../models/db'

const {performance} = require('perf_hooks');

module.exports = {
    create,
    get,
    remove,
    update
};

async function create(request) {
    let t0 = performance.now()

    if (!request.GUID) throw 'No GUID'
    if (!request.grades) throw 'No grade'

    const user = new GUID(request);

    await user.save()
    let t1 = performance.now()
    return {...user.toJSON(), time: t1 - t0}
}


async function update(req) {
    let t0 = performance.now()
    if (!req.GUID) throw 'No GUID'
    if (!req.grades) throw 'No grade'

    const user = await GUID.findOne({GUID: req.GUID});
    if (!user) throw 'User not found'

    user.grade = req.grade

    await user.save()

    let t1 = performance.now()
    return {...user.toJSON(), time: t1 - t0}
}

async function get(req) {
    let t0 = performance.now()
    if (req.GUID) {
        let u = await GUID.find({GUID: req.GUID});
        let t1 = performance.now()
        return {u, time: t1 - t0}
    } else if (req.grade) {
        let u = await GUID.find({grade: req.grade})
        let t1 = performance.now()
        return {u, time: t1 - t0}
    } else throw 'No params!'
}


async function remove(req) {
    let t0 = performance.now()
    let u = await GUID.findOneAndRemove({GUID: req.GUID});
    let t1 = performance.now()
    return {u, time: t1 - t0}
}




