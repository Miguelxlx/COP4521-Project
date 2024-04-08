import dotenv from 'dotenv';
import path from 'path';
import connectDB from './config/db.js';
import express from 'express';
import { errorHandler } from './middleware/errorMiddleware.js';
import userRoutes from './routes/userRoutes.js';
import cookieParser from 'cookie-parser';

dotenv.config();
const port = process.env.PORT || 5000;
const app = express();

// Body parser middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Cookie parser middleware
app.use(cookieParser());

const __dirname = path.resolve();
app.use('/uploads', express.static(path.join(__dirname, '/uploads')));

if (process.env.NODE_ENV === 'production') {
    app.use(express.static(path.join(__dirname, '/frontend/build')));
    app.get('*', (req,res) => res.sendFile(path.resolve(__dirname, 'frontend', 'build', 'index.html')));
} else {
    app.get('/', (req, res) => {
        res.send('API is running...');
    });
}

// Error handler
app.use(errorHandler);

// Use routes
app.use('/api/users', userRoutes);

// Connect to MongoDB and then start the server
connectDB().then(() => {
    app.listen(port, () => {
        console.log(`Server running on port ${port}`);
        console.log(`MongoDB Connected: ${process.env.MONGO_URI}`);
    });
}).catch(error => {
    console.error(`Error connecting to MongoDB: ${error.message}`);
    process.exit(1);
});
