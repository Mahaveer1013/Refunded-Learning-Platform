import express from 'express';
import axios from 'axios';

const app = express();
app.use(express.json()); // Parse JSON payloads

const LOCAL_SERVER_URL = 'http://127.0.0.1:8000/webhook/razorpay'; // Your local backend URL

app.post('/webhook/razorpay', async (req, res) => {
    try {
        console.log("🔹 Received Webhook from Razorpay");
        console.log(req.body);

        // Forward request as-is, including headers
        const razorpayHeaders = req.headers;

        const response = await axios.post(LOCAL_SERVER_URL, req.body, {
            headers: { ...razorpayHeaders } // Forward all headers
        });

        console.log("✅ Webhook forwarded successfully");
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error("❌ Error Forwarding Webhook:", error.message);
        res.status(500).send('Failed to forward webhook');
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 Proxy Server Running on port ${PORT}`));
