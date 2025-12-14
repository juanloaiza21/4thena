export default () => ({
    port: parseInt(process.env.PORT || '3000', 10),
    database: {
        MONGO_URI: process.env.MONGO_URI,
    },
    mq: {
        NATS_URI: process.env.NATS_URI,
    },
    email: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS,
    },
    twilio: {
        accountSid: process.env.TWILIO_ACCOUNT_SID,
        authToken: process.env.TWILIO_AUTH_TOKEN,
    },
});
