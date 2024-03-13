import dotenv from 'dotenv';
import path from 'path';
dotenv.config();
import connectDB from './config/db.js';
import express from 'express';
import cookieParser from 'cookie-parser';
import { notFound, errorHandler } from './middleware/errorMiddleware.js';

const port = process.env.PORT || 5000;

connectDB();

const app = express();

//Body parser middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//Cookie parser middleware
app.use(cookieParser());

const __dirname = path.resolve();
if (process.env.NODE_ENV === 'production'){
    //set static folder
    app.use(express.static(path.join(__dirname, '/frontend/build')));

    // any route that is not api will be redirected to index.html
    app.get('*', (req,res) => res.sendFile(path.resolve(__dirname, 'frontend', 'build', 'index.html')));
 } else {
    app.get('/', (req, res) => {
        res.send('API is running...');
     });
 }

 app.use(notFound);
 app.use(errorHandler);
 
 app.listen(port, () => console.log(`Server running on port ${port}`));

