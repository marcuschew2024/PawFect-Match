const functions = require('firebase-functions');
const axios = require('axios');

// Your external API keys
const DOG_API_KEY = 'live_m9FVcETQaok0LTSqCHAJrMMvkhBAIF2PfmvUMfwKq7n3zQIcDuHndLIerVPtmKEH';
const CAT_API_KEY = 'live_m9FVcETQaok0LTSqCHAJrMMvkhBAIF2PfmvUMfwKq7n3zQIcDuHndLIerVPtmKEH';

const cors = require('cors')({ origin: true });

// Convert your Flask routes to Firebase Functions
exports.getDogBreeds = functions.https.onRequest(async (req, res) => {
  // Set CORS headers
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    const response = await axios.get('https://api.thedogapi.com/v1/breeds', {
      headers: { 'x-api-key': DOG_API_KEY }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching dog breeds:', error);
    res.status(500).json({ error: 'Failed to fetch dog breeds' });
  }
});

exports.getCatBreeds = functions.https.onRequest(async (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    const response = await axios.get('https://api.thecatapi.com/v1/breeds', {
      headers: { 'x-api-key': CAT_API_KEY }
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching cat breeds:', error);
    res.status(500).json({ error: 'Failed to fetch cat breeds' });
  }
});

exports.getDogImages = functions.https.onRequest(async (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    const breedId = req.query.breed_id;
    const limit = req.query.limit || 1;
    
    const params = { limit, size: 'med' };
    if (breedId) params.breed_ids = breedId;
    
    const response = await axios.get('https://api.thedogapi.com/v1/images/search', {
      headers: { 'x-api-key': DOG_API_KEY },
      params
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching dog images:', error);
    res.status(500).json({ error: 'Failed to fetch dog images' });
  }
});

exports.getCatImages = functions.https.onRequest(async (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  try {
    const breedId = req.query.breed_id;
    const limit = req.query.limit || 1;
    
    const params = { limit, size: 'med' };
    if (breedId) params.breed_ids = breedId;
    
    const response = await axios.get('https://api.thecatapi.com/v1/images/search', {
      headers: { 'x-api-key': CAT_API_KEY },
      params
    });
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching cat images:', error);
    res.status(500).json({ error: 'Failed to fetch cat images' });
  }
});