<template>
  
  <div class="houses-container">
        <!-- Edit form -->
        <div v-if="editingHouse">
      <h2>Edit House</h2>
      <form @submit.prevent="updateHouse">
        <input v-model="editingHouse.ID" type="hidden" />
        <label for="house_address">Address:</label>
        <input v-model="editingHouse.house_address" type="text" id="house_address" required />
        
        <label for="zip_code">ZIP Code:</label>
        <input v-model="editingHouse.zip_code" type="text" id="zip_code" required />
        
        <label for="price">Price:</label>
        <input v-model="editingHouse.price" type="number" id="price" required />
        
        <label for="beds">Beds:</label>
        <input v-model="editingHouse.beds" type="number" id="beds" required />
        
        <label for="baths">Baths:</label>
        <input v-model="editingHouse.baths" type="number" step="0.1" id="baths" required />
        
        <label for="sqft">Square Feet:</label>
        <input v-model="editingHouse.sqft" type="number" id="sqft" required />
        
        <label for="property_type">Property Type:</label>
        <input v-model="editingHouse.property_type" type="text" id="property_type" required />
        
        <label for="current_status">Status:</label>
        <input v-model="editingHouse.current_status" type="text" id="current_status" required />
        
        <label for="image_link">Image Link:</label>
        <input v-model="editingHouse.image_link" type="text" id="image_link" />
        
        <button type="submit">Update</button>
      </form>
    </div>
    <div v-for="house in houses" :key="house.house_address" class="house-card">
      <img :src="house.image_link" alt="House Image" class="house-image" />
      <div class="house-details">
        <h2>{{ house.house_address }}</h2>
        <p><strong>Price:</strong> ${{ house.price.toLocaleString() }}</p>
        <p><strong>Beds:</strong> {{ house.beds }}</p>
        <p><strong>Baths:</strong> {{ house.baths }}</p>
        <p><strong>Square Feet:</strong> {{ house.sqft.toLocaleString() }}</p>
        <p><strong>Property Type:</strong> {{ house.property_type }}</p>
        <p><strong>Status:</strong> {{ house.current_status }}</p>
        <p><strong>ZIP Code:</strong> {{ house.zip_code }}</p>
      </div>
      <button @click="editHouse(house)">Edit</button>
      <button @click="deleteHouse(house.ID)">Delete</button>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      houses: [],          // List of houses
      editingHouse: null   // Currently editing house
    };
  },
  async created() {
    this.houses = await this.fetchHouses(); // Fetch data when component is created
  },
  methods: {
  async fetchHouses() {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/houses/');
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      return data; // Return the fetched data
    } catch (error) {
      console.error('Fetch error:', error);
      return [];
    }
  },

  editHouse(house) {
    this.editingHouse = { ...house }; // Copy house data for editing, spread operator
  },
  async deleteHouse(id) {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/houses/', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ id })
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        this.houses = this.houses.filter(house => house.ID !== id);
      } catch (error) {
        console.error('Delete error:', error);
      }},
  async updateHouse() {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/houses/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id: this.editingHouse.ID, 
          house_address: this.editingHouse.house_address,
          zip_code: this.editingHouse.zip_code,
          price: this.editingHouse.price,
          beds: this.editingHouse.beds,
          baths: this.editingHouse.baths,
          sqft: this.editingHouse.sqft,
          property_type: this.editingHouse.property_type,
          current_status: this.editingHouse.current_status,
          image_link: this.editingHouse.image_link
        })
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const updatedHouse = await response.json();
      const index = this.houses.findIndex(house => house.ID === updatedHouse.house.ID);
      if (index !== -1) {
        this.houses.splice(index, 1, updatedHouse.house);
      }
      this.editingHouse = null; 
    } catch (error) {
      console.error('Update error:', error);
    }
  }
}
};
</script>
<style scoped>
.houses-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.house-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  width: 300px;
}

.house-image {
  width: 100%;
  height: auto;
}

.house-details {
  padding: 16px;
}

.house-details h2 {
  margin-top: 0;
  font-size: 1.25em;
}

.house-details p {
  margin: 4px 0;
}
</style>