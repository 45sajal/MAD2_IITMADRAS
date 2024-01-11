
  <template>
    <div class="container mt-5">
      <h1 class="text-center">Checkout</h1>
  
      <h2 class="items">Items in Cart</h2>
      <ul class="list-group">
        <li v-for="cartItem in cartItems" :key="cartItem.id" class="list-group-item">
          {{ cartItem.product_name }} - Quantity: {{ cartItem.product_qty }} - Amount: {{ cartItem.amount }}
        </li>
      </ul>
  
      <h2 class="amount">Total Amount: {{ totalAmount }}</h2>
  
      <form @submit.prevent="confirmCheckout">
        <button class="btn btn-primary" type="submit">Confirm Checkout</button>
      </form>
  
      <router-link :to="`/user_after_login`" class="btn btn-secondary">Back to Dashboard</router-link>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        cartItems:[],
        totalAmount:''
      }
    },
    mounted() {
        this.fetchproducts()
    },
    methods: {
      confirmCheckout() {
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
          console.error("Access token not found.");
          return;
        }
        axios
          .post(`http://localhost:5000/checkout/${this.$route.params.username}`,{},{
            headers: { Authorization: `Bearer ${accessToken}` }
          })
          .then((response) => {
            const data = response.data;
            this.$router.push('/');
            console.log("Checkout confirmed", data);
        
          })
          .catch((error) => {
            console.error("Error confirming checkout", error);
            
          });
      },
      fetchproducts() {
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
          console.error("Access token not found.");
          return;
        }
        axios.get(`http://localhost:5000/checkout/${this.$route.params.username}`,{ headers: { Authorization: `Bearer ${accessToken}` }})
        .then((response) => {
            this.cartItems = response.data.cartItems;
            this.totalAmount = response.data.totalAmount
        })
        .catch(error => {
          console.error(error);
          
        });
      }
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

.mt-5 {
  margin-top: 3rem;
}

.list-group {
  margin-top: 20px;
}

.list-group-item {
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
  color:yellow
}

.amount{
  color:rgb(4, 251, 131);
}
.items{
  color:yellow;
}

.btn {
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
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
</style>
  


