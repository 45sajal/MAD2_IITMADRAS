<!-- <template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="manager">
      <label>Username:</label>
      <input v-model="username" type="text" required>
      <label>Password:</label>
      <input v-model="password" type="password" required>
      <button type="submit">Login</button>
    </form>
    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template> -->

<template>
  <div class="login-container">
    <h2 class="login-title">Login</h2>
    <form @submit.prevent="manager" class="login-form">
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
    manager() {
      const userData = {
        m_name: this.username,
        m_password: this.password
      };

      axios.post('http://localhost:5000/login_manager', userData)
        .then(response => {
          console.log('Login successful');
          
          localStorage.setItem('access_token', response.data.access_token);
          isAuthenticated.value = true;
          this.$router.push('/manager_after_login');
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

.login-title {
  text-align: center;
  color: #333;
}

.login-form {
  margin-top: 20px;
}

.login-label {
  display: block;
  margin-bottom: 8px;
  color: #333;
}

.login-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.login-button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>