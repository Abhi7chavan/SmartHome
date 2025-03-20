const { Kafka } = require('kafkajs');
const { Server } = require('socket.io');

const clientId = 'ems-household-manager';
const groupId = 'kitchen-appliances-group';
const topic = 'energy';
const kafka = new Kafka({
    clientId: clientId,
    brokers: ['localhost:9092'],
});

const consumer = kafka.consumer({ groupId });

const setupKafkaConsumer = async (io) => {
    await consumer.connect();
    await consumer.subscribe({ topic, fromBeginning: true });

    await consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
            const rawData = message.value.toString();
            io.emit('message', rawData); // Broadcasting data to clients
        },
    });
};

// Export function so it can be used in server.js
module.exports = setupKafkaConsumer;
