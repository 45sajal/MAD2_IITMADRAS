<template>
  <div class="login-container">
    <h2 class="login-heading">Login</h2>
    <form @submit.prevent="login" class="login-form">
      <label class="login-label">Username:</label>
      <input v-model="username" type="text" class="login-input" required>
      <label class="login-label">Password:</label>
      <input v-model="password" type="password" class="login-input" required>
      <button type="submit" class="login-button">Login</button>
    </form>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios';
import { isAuthenticated } from '@/router';
export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },
  methods: {
    login() {
      const userData = {
        username: this.username,
        password: this.password
      };

      axios.post('http://localhost:5000/login', userData)
        .then(response => {
          console.log('Login successful');
          
          localStorage.setItem('access_token', response.data.access_token);
          
          isAuthenticated.value = true;
          this.$router.push('/user_after_login');
        })
        .catch(error => {
          console.error('Login failed:', error.response.data.message);
          this.error = 'Invalid credentials. Please check your username and password.';
        });
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-heading {
  font-size: 24px;
  margin-bottom: 20px;
  color:black;
}

.login-form {
  display: grid;
  gap: 10px;
}

.login-label {
  font-size: 16px;
  color:black;
}

.login-input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 3px;
  outline: none;
}

.login-button {
  background-color: #4caf50;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #2980b9;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
}
</style>