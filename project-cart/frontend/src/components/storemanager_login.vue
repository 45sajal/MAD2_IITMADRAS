
<!-- <template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="login">
        <label for="name">Username:</label>
        <input v-model="name" type="name" required>
        <label for="password">Password:</label>
        <input v-model="password" type="password" required>
        <button type="submit">Login</button>
      </form>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </template> -->
  <template>
    <div>
      <h2 class="text-center">Login</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="name">Username:</label>
          <input v-model="name" type="text" class="form-control" required>
        </div>
  
        <div class="form-group">
          <label for="password">Password:</label>
          <input v-model="password" type="password" class="form-control" required>
        </div>
  
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
  
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import { isAuthenticated } from '@/router';
  export default {
    data() {
      return {
        name: '',
        password: '',
        error: null,
      };
    },
    methods: {
      login() {
        axios.post('http://localhost:5000/store_manager_login', {
          name: this.name,
          password: this.password,
        })
        .then(response => {
          localStorage.setItem('access_token', response.data.access_token);
          console.log('Login successful:', response.data);
          isAuthenticated.value = true;
          this.$router.push({name:'Storemanager_After_Login'})
        })
        .catch(error => {
          console.error('Login failed:', error.response.data);
          this.error = 'Invalid credentials. Please check your username and password.';
        });
      },
    },
  };
  </script>

<style scoped>
.text-center {
  text-align: center;
}

.login-form {
  max-width: 400px;
  margin: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 8px;
}

.btn {
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
}

.btn-primary {
  background-color: green;
  color: white;
}

.btn-primary:hover {
  background-color: rgb(3, 36, 3);
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
  