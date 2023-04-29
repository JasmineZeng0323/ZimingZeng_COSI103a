const express = require('express');
const { generateImage } = require('../controllers/openaiController');
const router = express.Router();


isLoggedIn = (req,res,next) => {
  if (res.locals.loggedIn) {
    next()
  } else {
    res.redirect('/login')
  }
}

router.post('/generateimage',isLoggedIn, generateImage);

router.get('/openai/:itemId',isLoggedIn, (req,res) => {
  if(req.params.itemId=='0'){

    res.render("aiImage")
  }
});

module.exports = router;