var express = require('express');
var router = express.Router();
const {
    check,
    body,
    validationResult
} = require('express-validator');

var db = require('../db')

router.get('/:id', async function(req, res, next) {
    const item = await db.query('select * from inventory where id = ' + req.params.id);
    const category = await db.query('select * from categories where id = ' + item.rows[0].categoryid);
    const experts = await db.query('select * from experts where expertfor = ' + req.params.id)
    res.render('item', {
        title: 'Item',
        linkActive: 'item',
        item: item.rows[0],
        category: category.rows[0],
        experts: experts.rows
    });
});

router.get('/addExpert/:id', async function(req, res, next) {
    const item = await db.query('select * from inventory where id = ' + req.params.id);
    res.render('addExpert', {
        title: 'AddExpert',
        linkActive: 'addExpert',
        item: item.rows[0]
    });
});

router.post('/addExpert/:id', [
    body('name')
    .not().isEmpty()
    .trim().isLength({min: 3, max: 20}),
    body('surname')
    .not().isEmpty()
    .trim().isLength({min: 3, max: 20}),
    body('employedsince')
    .not().isEmpty()
    .trim().isInt({min: 1970, max: 2021}).toInt(),
    body('expertsince')
    .not().isEmpty()
    .trim().isInt({min: 1970, max: 2021}).toInt(),
    body('email')
    .not().isEmpty()
    .trim().isEmail().normalizeEmail()
], async function (req, res, next) {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        // res.status(422).send(
        //     JSON.stringify(errors.array())
        // );
        res.render('error', {
            title: "Add expert (error)",
            linkActive: "Error",
            itemID: req.params.id,
            errors: JSON.stringify(errors.array())
        });
    } else {
        try {
            //console.log('insert into experts (name, surname, email, employedsince, expertsince, expertfor) values ('+ req.body.name + ',' +req.body.surname + ',' + req.body.email + ',' + req.body.employedsince + ',' + req.body.expertsince + ',' + req.params.id + ');')
            await db.query('insert into experts (name, surname, email, employedsince, expertsince, expertfor) values ($1, $2, $3, $4, $5, $6)', [req.body.name, req.body.surname, req.body.email, req.body.employedsince, req.body.expertsince, 2],)
            res.redirect('/item/<%= req.params.id %>');
        } catch (err) {
            res.render('error', {
                title: "Add expert (error)",
                linkActive: "Error",
                itemID: req.params.id,
                errors: JSON.stringify(errors.array())
            });
        }
    }
});


module.exports = router;
