import {GUID, Subject} from '../models/db'

const {performance} = require('perf_hooks');

module.exports = {
    create,
    get,
    remove,
    update
};

async function create(request) {


    if (!request.GUID) throw 'No GUID'
    if (!request.subject) throw 'No subject'
    if (!request.grade) throw 'No grade'

    let t0 = performance.now()
    let user = await GUID.findOne({GUID: request.GUID}).populate({path: 'subjects'});
    if (user) return {user: null, time: t1 - t0}

    const subject = new Subject({subjectName: request.subject, grade: request.grade})
    await subject.save()

    user = new GUID({GUID: request.GUID, subjects: [subject.id]});

    await user.save()

    let t1 = performance.now()
    return {...user.toJSON(), time: t1 - t0}
}


async function update(request) {
    
    if (!request.GUID) throw 'No GUID'
    if (!request.subject) throw 'No subject'
    if (!request.grade) throw 'No grade'
    let t0 = performance.now()
    const user = await GUID.findOne({GUID: request.GUID}).populate({path: 'subjects'});
    if (!user) throw 'User not found'

    let found = false
    for (const subject of user.subjects) {
        if (subject.subjectName === request.subject) {
            let sub = await Subject.findById(subject.id)
            sub.grade = request.grade
            await sub.save()
            found = true
            break
        }
    }

    if (!found) {
        let sub = new Subject({subjectName: request.subject, grade: request.grade})
        sub.grade = request.grade
        await sub.save()
        user.subjects.push(sub.id)
    }

    await user.save()

    let t1 = performance.now()
    return {...user.toJSON(), time: t1 - t0}
}

async function get(req) {
    console.log(req)
    if (!req.GUID) throw 'need guid'
    let t0 = performance.now()
    let u = await GUID.find({GUID: req.GUID}).populate({path: 'subjects'});
    let t1 = performance.now()
    return {u, time: t1 - t0}
}


async function remove(req) {
    let t0 = performance.now()
    let u = await GUID.findOneAndRemove({GUID: req.GUID});
    let t1 = performance.now()
    return {u, time: t1 - t0}
}




