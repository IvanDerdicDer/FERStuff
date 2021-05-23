var express = require('express');
var router = express.Router();
var db = require('../db')

router.get('/:id', async function(req, res, next) {
    const item = await db.query('select * from inventory where id = ' + req.params.id);
    const category = await db.query('select * from categories where id = ' + item.rows[0].categoryid);
    res.render('item', {
        title: 'Item',
        linkActive: 'item',
        item: item.rows[0],
        category: category.rows[0]
    });
});

module.exports = router;
