require('dotenv').config();
const express = require('express');
const cors = require('cors');
const petsRouter = require('./routes/pets');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
    origin: ['http://localhost:5173', 'http://localhost:3000'],
    credentials: true
}));
app.use(express.json());

// Routes
app.use('/api/pets', petsRouter);

// Health check
app.get('/api/health', (req, res) => {
    res.json({ 
        message: 'Backend is running!', 
        database: 'Supabase',
        timestamp: new Date().toISOString() 
    });
});

// Test database connection
app.get('/api/test-db', async (req, res) => {
    try {
        const supabase = require('./config/supabase');
        const { data, error } = await supabase
            .from('pets')
            .select('count')
            .limit(1);
        
        if (error) throw error;
        
        res.json({ 
            message: 'Database connection successful',
            connected: true 
        });
    } catch (error) {
        res.status(500).json({ 
            message: 'Database connection failed',
            error: error.message 
        });
    }
});

app.listen(PORT, () => {
    console.log(`Backend server running on http://localhost:${PORT}`);
    console.log('Using Supabase as database');
});