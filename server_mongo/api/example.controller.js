const express = require('express');
const router = express.Router();
const exampleService = require('../services/example.service');


// define routes
router.post('/create', create);
router.get('/get', get);
router.put('/update', update)
router.delete('/delete', del)

module.exports = router;

function create(req, res, next) {
    /**
     * ExpressJS function to create a record object
     */
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
    /**
     * ExpressJS function to get a record object
     */
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
    /**
     * ExpressJS function to update a record object
     */
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
    /**
     * ExpressJS function to delete a record object
     */
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
