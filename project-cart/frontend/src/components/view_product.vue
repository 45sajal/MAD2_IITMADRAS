<!-- <template>
  <div class="container mt-5">
    <h2>List of all products</h2>
    <table class="table">
      <thead>
        <tr>
          <th>SNo</th>
          <th>Product_Name</th>
          <th>Product_Manufacture</th>
          <th>Product_Expiry</th>
          <th>Product_Per_Unit</th>
          <th>Product_Unit</th>
          <th>Product_Stock</th>
          <th>Section_ID</th>
          <th>Update_Product</th>
          <th>Delete_Product</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product, index in products" :key="product.id">
          <td>{{ product.id }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.manufacture }}</td>
          <td>{{ product.expiry }}</td>
          <td>{{ product.per_unit }}</td>
          <td>{{ product.unit }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ product.section }}</td>
          <td>
            <form @submit.prevent="updateProduct(product.id, index)">
              <div class="form-group">
                <label for="product_name">Product Name:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productName" required>
              </div>

              <div class="form-group">
                <label for="product_manufacture_date">Manufacture Date:</label>
                <input type="date" class="form-control" v-model="updateForms[index].productManufacture" required>
              </div>

              <div class="form-group">
                <label for="product_expiry_date">Expiry Date:</label>
                <input type="date" class="form-control" v-model="updateForms[index].productExpiry" required>
              </div>

              <div class="form-group">
                <label for="product_rate_per_unit">Rate per Unit:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productPerUnit" required>
              </div>

              <div class="form-group">
                <label for="product_unit">Product Unit:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productUnit" required>
              </div>

              <div class="form-group">
                <label for="product_stock">Product Stock:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productStock" required>
              </div>

            

              <button type="submit" class="btn btn-primary">Update Product</button>
            </form>
          </td>
          <td>
            <button @click="deleteProduct(product.id)" class="btn btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template> -->


<template>
  <div class="container mt-5">
    <h2>List of all products</h2>
    <table class="table">
      <thead>
        <tr>
          <th>SNo</th>
          <th>Product_Name</th>
          <th>Product_Manufacture</th>
          <th>Product_Expiry</th>
          <th>Product_Per_Unit</th>
          <th>Product_Unit</th>
          <th>Product_Stock</th>
          <th>Section_ID</th>
          <th>Update_Product</th>
          <th>Delete_Product</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product, index in products" :key="product.id">
          <td>{{ product.id }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.manufacture }}</td>
          <td>{{ product.expiry }}</td>
          <td>{{ product.per_unit }}</td>
          <td>{{ product.unit }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ product.section }}</td>
          <td>
            <form @submit.prevent="updateProduct(product.id, index)">
              <div class="form-group">
                <label for="product_name">Product Name:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productName" required>
              </div>

              <div class="form-group">
                <label for="product_manufacture_date">Manufacture Date:</label>
                <input type="date" class="form-control" v-model="updateForms[index].productManufacture" required>
              </div>

              <div class="form-group">
                <label for="product_expiry_date">Expiry Date:</label>
                <input type="date" class="form-control" v-model="updateForms[index].productExpiry" required>
              </div>

              <div class="form-group">
                <label for="product_rate_per_unit">Rate per Unit:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productPerUnit" required>
              </div>

              <div class="form-group">
                <label for="product_unit">Product Unit:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productUnit" required>
              </div>

              <div class="form-group">
                <label for="product_stock">Product Stock:</label>
                <input type="text" class="form-control" v-model="updateForms[index].productStock" required>
              </div>

              <button type="submit" class="btn btn-primary">Update Product</button>
            </form>
          </td>
          <td>
            <button @click="deleteProduct(product.id)" class="btn btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import axios from 'axios';
import { isAuthenticated } from '@/router';

export default {
  data() {
    return {
      products: [],
      updateForms: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  watch: {
    products: {
      handler(newProducts) {
        this.updateForms = newProducts.map(() => ({
          productName: '',
          productManufacture: '',
          productExpiry: '',
          productPerUnit: '',
          productUnit: '',
          productStock: '',
        }));
      },
      immediate: true,
    },
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/view_product');
        this.products = response.data;
        isAuthenticated.value = true;
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    deleteProduct(productId) {
      axios.delete(`http://127.0.0.1:5000/view_product/${productId}/delete`)
        .then(response => {
          console.log(response.data.message);
          this.$router.push('/storemanager_after_login');
        })
        .catch(error => {
          console.error(error);
        });
    },
    async updateProduct(productId, index) {
      try {
        const formattedManufactureDate = new Date(this.updateForms[index].productManufacture).toISOString().split('T')[0];
        const formattedExpiryDate = new Date(this.updateForms[index].productExpiry).toISOString().split('T')[0];
        const response = await axios.post(`http://127.0.0.1:5000/view_product/${productId}/update`, {
          product_name: this.updateForms[index].productName,
          product_manufacture_date:formattedManufactureDate,
          product_expiry_date: formattedExpiryDate,
          product_rate_per_unit: this.updateForms[index].productPerUnit,
          product_unit: this.updateForms[index].productUnit,
          product_stock: this.updateForms[index].productStock,
          
        });
        console.log(response.data);
        this.$router.push('/storemanager_after_login');
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>


<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); */
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table, th, td {
  border: 1px solid #ccc;
}

th, td {
  padding: 10px;
  text-align: left;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger:hover {
  background-color: #bd2130;
}
</style>
