const express = require('express');
const router = express.Router();
const dummyService = require('../../services/dummy.service');

router.post('/create', create);
router.get('/get', get);
router.put('/update', update)
router.delete('/delete', del)

module.exports = router;

function create(req, res, next) {
    dummyService.create(req.body)
        .then((obj) => {
            if (obj) {
                res.status(200).json(obj)
            }
        }).catch((err) => {
        res.status(400)
        console.log(err)
        next(err)
    });
}

function get(req, res, next) {

}

function update(req, res, next) {
}


function del(req, res, next) {

}
