<template>
  <div class="product-search-container">
    <h2 class="mt-4">Search for Products</h2>
    <form @submit.prevent="searchProducts" class="form-inline">
      <div class="input-group mb-3">
        <input v-model="searchQuery" type="text" class="form-control" name="item" placeholder="Enter product name" aria-label="Search product">
        <div class="input-group-append">
          <button class="btn btn-primary" type="submit">Search</button>
        </div>
      </div>
    </form>
  </div>

  <div class="product-list-container">
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <table class="table">
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Manufacture Date</th>
          <th>Expiry Date</th>
          <th>Rate</th>
          <th>Unit</th>
          <th>Stock</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.product_id">
          <td>{{ item.product_name }}</td>
          <td>{{ item.product_manufacture_date }}</td>
          <td>{{ item.product_expiry_date }}</td>
          <td>{{ item.product_rate_per_unit }}</td>
          <td>{{ item.product_unit }}</td>
          <td>{{ item.product_stock }}</td>
          <!-- <td>{{ displayStock[item.product_id] }}</td> -->
          <td>
            <div v-if="item.product_stock > 0">
              <form @submit.prevent="addToCart(item)">
                <input v-model="itemQuantities[item.product_id]" type="number" class="form-control" name="product_qty" min="1">
                <input type="hidden" name="product_id" :value="item.product_id">
                <button type="submit" class="btn btn-success" >Add to Cart</button>
                <!-- <button type="submit" class="btn btn-success" :disabled="displayStock[item.product_id] <= 0">Add to Cart</button> -->
              </form>
            </div>
            <div v-else>
              <button type="button" class="btn btn-danger" disabled>Out of Stock</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  <script>
  import axios from 'axios';

  export default{
    data(){
        return{
            items:[],
            itemQuantities: {},
            searchQuery: '', 
            uname:'',
            error: null,
            // displayStock: {}, 
        }
    },
    mounted() {
      const accessToken = localStorage.getItem("access_token");
    this.fetchProducts();
  },
  methods:{
    fetchProducts() {
      const sectionId = this.$route.params.sectionId;
     
      axios.get(`http://127.0.0.1:5000/section/${sectionId}/products`)
        .then((response) => {
          this.items = response.data.items;
        this.items.forEach((item) => {
          this.displayStock[item.product_id] = item.product_stock;
        });
        })
        .catch((error) => {
          console.error('Error fetching products:', error);
        });
    },
    searchProducts(){

    },
    addToCart(item) {
      const accessToken = localStorage.getItem("access_token");
    if (item && item.product_id) {
      const product_id = item.product_id;
      const product_qty = this.itemQuantities[product_id];

      if (!(product_qty && Number.isInteger(product_qty) && product_qty > 0)) {
        console.error("Invalid product quantity");
        return;
      }

    // const updatedDisplayStock = { ...this.displayStock };
    // updatedDisplayStock[product_id] -= product_qty;

    // // Assign the updated displayStock to trigger reactivity
    // this.displayStock = updatedDisplayStock


      axios.post(`http://127.0.0.1:5000/products/${product_id}/add_to_cart`, { product_id, product_qty },
        {headers: {
            Authorization: `Bearer ${accessToken}`,
          }
       })
        .then(response => {
          console.log(response.data);
          this.$router.push('/cart');
        })
        .catch(error => {
          if (error.response && error.response.data) {
              this.error = error.response.data.message;
            } else {
              this.error = 'An error occurred while adding to cart.';
            }
          // console.error(error.response.data);
        });
    } else {
      console.error("Item or product_id is undefined");
    }
  }
  }
  }
</script>

<style scoped>
.product-search-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.product-list-container {
  margin-top: 20px;
  background-color: white;
  color:black;
}

.form-inline {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.table th {
  background-color: #f2f2f2;
}

.btn-success {
  background-color: #28a745;
  color: black;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.btn-success:hover {
  opacity: 0.8;
  background-color: yellow;
}
</style>