const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const { authenticate } = require('../middleware/authMiddleware');

router.use(authenticate);

router.get('/dashboard', adminController.getDashboardData);

module.exports = router;
