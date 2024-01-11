

<template>
  <div class="signup-container">
    <h2 class="signup-heading">Signup</h2>
    <form @submit.prevent="signup" class="signup-form">
      <label class="signup-label">Username:</label>
      <input v-model="username" type="text" class="signup-input" required>
      <label class="signup-label">Password:</label>
      <input v-model="password" type="password" class="signup-input" required>
      <label class="signup-label">Email:</label>
      <input v-model="email" type="email" class="signup-input" required>
      <button type="submit" class="signup-button">Signup</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      email:'',
    };
  },
  methods: {
    signup() {
      const userData = {
        username: this.username,
        password: this.password,
        email:this.email,
      };

      axios.post('http://localhost:5000/signup', userData)
        .then(response => {
          console.log(response.data.message);
          this.$router.push('/login');
         
        })
        .catch(error => {
          console.error('Signup failed:', error.response.data.message);
        
        });
    }
  }
};
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.signup-heading {
  font-size: 24px;
  margin-bottom: 20px;
  color: black;
}

.signup-form {
  display: grid;
  gap: 10px;
}

.signup-label {
  font-size: 16px;
  color: black; /* Text color */
}

.signup-input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  border: none; /* Remove border */
  border-bottom: 1px solid #ccc; /* Add bottom border for separation */
  outline: none; /* Remove default focus outline */
}

.signup-button {
  background-color: #4caf50;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
.signup-button:hover {
  background-color: #3227ae; /* Darker green color for hover effect */
}

</style>