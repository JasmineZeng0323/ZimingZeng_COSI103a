// Import necessary modules
const express = require('express');
const mongoose = require('mongoose');

// Create express app
const app = express();

app.use(express.json())

// Connect to MongoDB using Mongoose
mongoose.connect('mongodb://localhost:27017/myapp', {
        useNewUrlParser: true,
        useUnifiedTopology: true
    })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));

// Define transaction schema
const transactionSchema = new mongoose.Schema({
    description: String,
    amount: Number,
    category: String,
    date: String,
});

// Define transaction model
const Transaction = mongoose.model('Transaction', transactionSchema);

// Define route to get all transactions
app.get('/transactions', async(req, res) => {
    try {
        const transactions = await Transaction.find();
        res.json(transactions);
    } catch (err) {
        res.status(500).send(err);
    }
});

// Define route to aggregate transactions by category and return category and sum of amount
app.get('/categories', async(req, res) => {
    try {
        const transactions = await Transaction.aggregate([{
            $group: {
                _id: "$category",
                amount: {
                    $sum: "$amount"
                },
                category: {
                    $first: "$category"
                }
            }
        }]);
        res.json(transactions);
    } catch (err) {
        res.status(500).send(err);
    }
});


// Define route to add a new transaction
app.post('/transactions', async(req, res) => {
    const {
        amount,
        date,
        description,
        category
    } = req.body;
    const trimmedCategory = category.trim();
    const transaction = new Transaction({
        description,
        amount,
        category: trimmedCategory,
        date
    });
    // console.log(transaction)

    try {
        const savedTransaction = await transaction.save();
        res.send('success')
    } catch (err) {
        res.status(500).send(err);
    }
});

// Define route to delete a transaction by ID
app.delete('/transactions/:id', async(req, res) => {
    const {
        id
    } = req.params;
    try {
        const deletedTransaction = await Transaction.findByIdAndDelete(id);
        if (!deletedTransaction) {
            return res.status(404).send('Transaction not found');
        }
        res.send('Transaction deleted successfully');
    } catch (err) {
        console.log(err)
        res.status(500).send(err);
    }
});


// Define route to update a transaction by ID
app.put('/transactions/:id', async(req, res) => {
    const {
        id
    } = req.params;
    const {
        amount,
        date,
        description,
        category
    } = req.body;
    try {
        const updatedTransaction = await Transaction.findByIdAndUpdate(id, {
            amount,
            date,
            description,
            category
        }, {
            new: true
        });
        if (!updatedTransaction) {
            return res.status(404).send('Transaction not found');
        }
        res.send(updatedTransaction);
    } catch (err) {
        console.log(err)
        res.status(500).send(err);
    }
});

// Serve index.html file on the root route
app.get('/transaction', async(req, res) => {
    res.sendFile(__dirname + '/index.html')
});

app.get('/transaction/byCategory', async(req, res) => {
    res.sendFile(__dirname + '/category.html')
});

// Start server
app.listen(3000, () => console.log('Server started'));