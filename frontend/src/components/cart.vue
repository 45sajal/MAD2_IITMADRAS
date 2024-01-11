  <template>
    <div class="container mt-5">
      <div v-if="userCart.length > 0">
        <h2>My Cart</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Quantity</th>
              <th>Amount</th>
              <th>Update Cart</th>
              <th>Delete from Cart</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in userCart" :key="item.item_id">
              <td>{{ item.product_name }}</td>
              <td>{{ item.product_qty }}</td>
              <td>{{ item.amount }}</td>
              <td>
                <router-link :to="'/update/' + item.product_name + '/' + item.item_id" class="btn btn-warning">Update Cart</router-link>
              </td>
              <td>
                <button @click="deleteFromCart(item.product_id, item.username)" class="btn btn-danger">Delete from Cart</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="checkout-button-container">
        <router-link :to="checkoutLink" class="btn btn-primary">Proceed to Checkout</router-link>
      </div>
      </div>
      <div v-else>
        <h1>Your cart is empty.</h1>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { isAuthenticated } from '@/router';
  export default {
    data() {
      return {

        userCart:[],
        uname:''
      };
    },
    mounted() {
      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        console.error("Access token not found.");
        return}
        this.fetchUserCart(accessToken)
      
    },
    methods: {
      deleteFromCart(product_id,username) {
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
          console.error("Access token not found.");
          return;
        }
        axios.delete(
        `http://localhost:5000/products/${product_id}/${username}/delete_from_cart`,
        { headers: { Authorization: `Bearer ${accessToken}` } }
      )
      .then(response => {
          this.userCart = response.data.user_cart;

        })
        .catch(error => {
          // Handle errors
          console.error('Error deleting from cart:', error);
        });
      },
      fetchUserCart(accessToken) {
       
        axios.get('http://localhost:5000/user/cart',{
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
          .then(response => {
            this.userCart = response.data.userCart; 
            this.uname = response.data.uname;
            isAuthenticated.value = true;
          })
          .catch(error => {
            console.error('Error fetching user cart:', error);
          });
      },
    },
    computed:{
      checkoutLink() {
     
      return `/checkout/${this.uname}`;
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

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: white;
  color: black;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.table th {
  background-color: #f2f2f2;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-warning {
  background-color: #ffc107;
  color:white
}

.btn-warning:hover {
  background-color: #e0a800;
}
.checkout-button-container {
  margin-top: 20px; 
}
</style>
 
  