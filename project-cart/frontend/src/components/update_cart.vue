
  <template>
    <div class="container mt-5">
      <h2 class="text-center">Update Cart Item</h2>
      <form @submit.prevent="updateCart" class="mt-4">
        <div class="mb-3">
          <label for="product_qty" class="form-label">New Quantity:</label>
          <input v-model="newQuantity" type="number" name="product_qty" min="1" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Update Cart</button>
      </form>
      <router-link to="/cart" class="btn btn-secondary mt-3">Back to Dashboard</router-link>
      <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
        {{ errorMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { isAuthenticated } from '@/router';
  export default {
    data() {
      return {
        newQuantity: 0,
        errorMessage: '',
      };
    },
    methods: {
      updateCart() {
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
          console.error("Access token not found.");
          
          return;
        }
  
        axios.post(`http://127.0.0.1:5000/update/${this.$route.params.uname}/${this.$route.params.item_id}`, {
          product_qty: this.newQuantity
        }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then(response => {
          
          console.log(response.data.message);
          isAuthenticated.value = true;
          this.$router.push('/cart');
        })
        .catch(error => {
          this.errorMessage = error.response.data.message;
          console.error(error.response.data.message);
        });
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
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.text-center {
  text-align: center;
  color:black
}

.mt-4 {
  margin-top: 1.5rem;
}

.mb-3 {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-control {
  width: 100%;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
}

.btn {
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  border-radius: 0.25rem;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.alert {
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
}
</style>