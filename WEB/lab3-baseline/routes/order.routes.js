var express = require('express');
var router = express.Router();
var db = require('../db')

router.get('/', async function(req, res, next) {
    const rows = await db.query('select * from categories')
    const inventoryRows = await db.query('select * from inventory');
    console.log(rows)
    res.render('order', {
        title: 'Order',
        linkActive: 'order',
        categoryRows: rows.rows,
        inventoryRows: inventoryRows.rows
    });
});

module.exports = router;

