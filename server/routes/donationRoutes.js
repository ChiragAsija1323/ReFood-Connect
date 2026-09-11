const express = require('express');
const router = express.Router();
const donationController = require('../controllers/donationController');
const { authenticate } = require('../middleware/authMiddleware');

router.use(authenticate); // Protect all donation routes

router.post('/', donationController.createDonation);
router.get('/', donationController.getDonations);
router.put('/:id', donationController.updateDonation);

module.exports = router;
