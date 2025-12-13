export default () => ({
    port: parseInt(process.env.PORT || '3000', 10),
    database: {
        MONGO_URI: process.env.MONGO_URI,
    },
});
