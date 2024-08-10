<template>
  <!-- npm install axios -->

  <div class="form-container">
      <h2>House Information Form</h2>
      <form @submit.prevent="submitForm">
          <label for="house_address">House Address:</label>
          <input type="text" v-model="form.house_address" required>

          <label for="zip_code">Zip Code:</label>
          <input type="text" v-model="form.zip_code" required>

          <label for="price">Price:</label>
          <input type="number" v-model.number="form.price" step="0.01" required>

          <label for="beds">Number of Beds:</label>
          <input type="number" v-model.number="form.beds" required>

          <label for="baths">Number of Baths:</label>
          <input type="number" v-model.number="form.baths" step="0.01" required>

          <label for="sqft">Square Footage:</label>
          <input type="number" v-model.number="form.sqft" required>

          <label for="property_type">Property Type:</label>
          <select v-model="form.property_type" required>
              <option value="House">House</option>
              <option value="Condo">Condo</option>
              <option value="Apartment">Apartment</option>
              <option value="Townhouse">Townhouse</option>
          </select>

          <label for="current_status">Current Status:</label>
          <select v-model="form.current_status" required>
              <option value="Sale">Sale</option>
              <option value="Sold">Sold</option>
              <option value="Pending">Pending</option>
              <option value="Rented">Rented</option>
          </select>

          <label for="image_link">Image Link:</label>
          <input type="url" v-model="form.image_link" placeholder="https://example.com/image.jpg">

          <button type="submit">Submit</button>
      </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
      return {
          form: {
              house_address: '',
              zip_code: '',
              price: 0,
              beds: 0,
              baths: 0,
              sqft: 0,
              property_type: '',
              current_status: '',
              image_link: ''
          }
      };
  },
  methods: {
      async submitForm() {
          try {
              const response = await axios.post('http://127.0.0.1:5000/api/houses/', this.form);
              console.log('Success:', response.data);
          } catch (error) {
              console.error('Error:', error);
          }
      }
  }
};
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}
.form-container h2 {
  text-align: center;
}
.form-container label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}
.form-container input, .form-container select {
  width: 100%;
  padding: 8px;
  margin-bottom: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-container button {
  width: 100%;
  padding: 10px;
  background-color: #6ba0dd;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}
.form-container button:hover {
  background-color: #6ba0dd;
}
</style>
