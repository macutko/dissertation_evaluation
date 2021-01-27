const express = require('express');
const router = express.Router();
const exampleService = require('../services/example.service');

router.post('/create', create);
router.get('/get', get);
router.put('/update', update)
router.delete('/delete', del)

module.exports = router;

function create(req, res, next) {
    exampleService.create(req.body)
        .then((obj) => {
            if (obj) {
                res.status(200).json(obj)
            }
        }).catch((err) => {
        res.status(400).json(err)
        console.log(err)
        next(err)
    });
}

function get(req, res, next) {
    exampleService.get(req.query)
        .then((obj) => {
            if (obj) {
                res.status(200).json(obj)
            }
        }).catch((err) => {
        res.status(400).json(err)
        console.log(err)
        next(err)
    });

}

function update(req, res, next) {
    exampleService.update(req.body)
        .then((obj) => {
            if (obj) {
                res.status(200).json(obj)
            }
        }).catch((err) => {
        res.status(400).json(err)
        console.log(err)
        next(err)
    });
}


function del(req, res, next) {
    exampleService.remove(req.query)
        .then((obj) => {
            if (obj) {
                res.status(200).json(obj)
            }
        }).catch((err) => {
        res.status(400).json(err)
        console.log(err)
        next(err)
    });

}
