const express = require('express');
const router = express.Router();
const supabase = require('../config/supabase');

// GET all pets
router.get('/', async (req, res) => {
  try {
    const { data: pets, error } = await supabase
      .from('pets')
      .select('*')
      .order('id', { ascending: true });

    if (error) {
      throw error;
    }

    res.json(pets);
  } catch (error) {
    console.error('Error fetching pets:', error);
    res.status(500).json({ 
      message: 'Error fetching pets from database',
      error: error.message 
    });
  }
});

// GET pet by ID
router.get('/:id', async (req, res) => {
  try {
    const { data: pet, error } = await supabase
      .from('pets')
      .select('*')
      .eq('id', req.params.id)
      .single();

    if (error) {
      throw error;
    }

    if (!pet) {
      return res.status(404).json({ message: 'Pet not found' });
    }

    res.json(pet);
  } catch (error) {
    console.error('Error fetching pet:', error);
    res.status(500).json({ 
      message: 'Error fetching pet from database',
      error: error.message 
    });
  }
});

// POST - Add new pet
router.post('/', async (req, res) => {
  try {
    const { name, age, breed, size, gender, furColor, personality, image, type } = req.body;

    // Validate required fields
    if (!name || !age || !breed || !size || !gender || !personality || !type) {
      return res.status(400).json({ 
        message: 'Missing required fields' 
      });
    }

    const { data: pet, error } = await supabase
      .from('pets')
      .insert([
        {
          name,
          age,
          breed,
          size,
          gender,
          fur_color: furColor,
          personality,
          image,
          type
        }
      ])
      .select()
      .single();

    if (error) {
      throw error;
    }

    res.status(201).json(pet);
  } catch (error) {
    console.error('Error creating pet:', error);
    res.status(500).json({ 
      message: 'Error creating pet in database',
      error: error.message 
    });
  }
});

// PUT - Update pet
router.put('/:id', async (req, res) => {
  try {
    const { name, age, breed, size, gender, furColor, personality, image, type } = req.body;

    const { data: pet, error } = await supabase
      .from('pets')
      .update({
        name,
        age,
        breed,
        size,
        gender,
        fur_color: furColor,
        personality,
        image,
        type,
        updated_at: new Date().toISOString()
      })
      .eq('id', req.params.id)
      .select()
      .single();

    if (error) {
      throw error;
    }

    if (!pet) {
      return res.status(404).json({ message: 'Pet not found' });
    }

    res.json(pet);
  } catch (error) {
    console.error('Error updating pet:', error);
    res.status(500).json({ 
      message: 'Error updating pet in database',
      error: error.message 
    });
  }
});

// DELETE - Remove pet
router.delete('/:id', async (req, res) => {
  try {
    const { error } = await supabase
      .from('pets')
      .delete()
      .eq('id', req.params.id);

    if (error) {
      throw error;
    }

    res.json({ message: 'Pet deleted successfully' });
  } catch (error) {
    console.error('Error deleting pet:', error);
    res.status(500).json({ 
      message: 'Error deleting pet from database',
      error: error.message 
    });
  }
});

// GET pets with filtering
router.get('/search/filter', async (req, res) => {
  try {
    const { type, size, gender, breed, search } = req.query;
    
    let query = supabase.from('pets').select('*');

    // Apply filters if provided
    if (type) query = query.eq('type', type);
    if (size) query = query.eq('size', size);
    if (gender) query = query.eq('gender', gender);
    if (breed) query = query.ilike('breed', `%${breed}%`);
    
    // Search across multiple fields
    if (search) {
      query = query.or(`name.ilike.%${search}%,breed.ilike.%${search}%,personality.ilike.%${search}%`);
    }

    query = query.order('id', { ascending: true });

    const { data: pets, error } = await query;

    if (error) {
      throw error;
    }

    res.json(pets);
  } catch (error) {
    console.error('Error filtering pets:', error);
    res.status(500).json({ 
      message: 'Error filtering pets',
      error: error.message 
    });
  }
});

module.exports = router;