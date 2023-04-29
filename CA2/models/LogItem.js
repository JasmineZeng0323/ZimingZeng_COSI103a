'use strict';
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

var LogItemSchema = Schema({
    user_id: String,
    url: String,
    method: String,
    body: String,
    params: String,
    ip_address: String,
    result: String,
    create_time: Date,
    updated_time: Date,
})

module.exports = mongoose.model('LogDoItem', LogItemSchema);
