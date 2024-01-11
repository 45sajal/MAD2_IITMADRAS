<!-- <template>
    <div class="container mt-5">
      <h1>Add Product</h1>
      <form @submit.prevent="createProduct" class="mt-4">
        <div class="form-group">
          <label for="p_name">Product Name:</label>
          <input v-model="productName" type="text" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_manufact">Product Manufacturing Date:</label>
          <input v-model="productManufact" type="date" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_expiry">Product Expiry Date:</label>
          <input v-model="productExpiry" type="date" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_perunit">Rate of Each Unit in ₹:</label>
          <input v-model="productPerUnit" type="number" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_unit">Unit of Product:</label>
          <input v-model="productUnit" type="text" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_stock">Remaining Stock of Product:</label>
          <input v-model="productStock" type="number" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_section">Section Name of Product:</label>
          <select v-model="productSection" class="form-control" required>
            <option v-for="section in sections" :key="section.id">{{ section.name }}</option>
          </select>
        </div>            
        <button type="submit" class="btn btn-primary">Create Product</button>
      </form>
    </div>
  </template> -->

  <template>
    <div class="container mt-5">
      <h1>Add Product</h1>
      <form @submit.prevent="createProduct" class="mt-4">
        <div class="form-group">
          <label for="p_name">Product Name:</label>
          <input v-model="productName" type="text" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_manufact">Product Manufacturing Date:</label>
          <input v-model="productManufact" type="date" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_expiry">Product Expiry Date:</label>
          <input v-model="productExpiry" type="date" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_perunit">Rate of Each Unit in ₹:</label>
          <input v-model="productPerUnit" type="number" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_unit">Unit of Product:</label>
          <input v-model="productUnit" type="text" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_stock">Remaining Stock of Product:</label>
          <input v-model="productStock" type="number" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="p_section">Section Name of Product:</label>
          <select v-model="productSection" class="form-control" required>
            <option v-for="section in sections" :key="section.id">{{ section.name }}</option>
          </select>
        </div>            
        <button type="submit" class="btn btn-primary">Create Product</button>
      </form>
    </div>
  </template>
  
<script>
import axios from 'axios';
// import { isAuthenticated } from '@/router';
export default {
  data() {
    return {
      productName:'',
      productManufact:'',
      productExpiry:'',
      productPerUnit:'',
      productUnit:'',
      productStock:'',
      productSection:'',
      sections: []
    };
  },
  mounted() {
    
    axios.get('http://127.0.0.1:5000/section_name')  
      .then(response => {
        this.sections = response.data;
      })
      .catch(error => {
        console.error(error);
      });
  },
  methods: {
    
    createProduct() {
      
      const productData={
        p_name:this.productName,
        p_manufact:this.productManufact,
        p_expiry:this.productExpiry,
        p_perunit:this.productPerUnit,
        p_unit:this.productUnit,
        p_stock:this.productStock,
        p_section:this.productSection,
      }
      
      axios.post('http://127.0.0.1:5000/add_product',productData) 
        .then(response => {
          console.log(response.data.message);
          // isAuthenticated.value = true;
          this.$router.push('/storemanager_after_login');
          
        })
        .catch(error => {
          console.error(error);
          
        });
    }
  }
};
</script>


<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-primary {
  background-color: #905907;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #3b2402;
}
</style>
  