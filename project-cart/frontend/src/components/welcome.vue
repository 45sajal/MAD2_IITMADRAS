

   <template>
    <div class="center-container">
      <div class="header">
        <h1 class="logo">Food Cart</h1>
      </div>
      <div class="navbar">
        <div class="nav-buttons">
          <button class="nav-btn" @click="signup">Signup</button>
          <button class="nav-btn" @click="login">Login</button>
          <button class="nav-btn" @click="manager_login">Manager Login</button>
          <button class="nav-btn" @click="storemanager_signup">Store Manager Signup</button>
          <button class="nav-btn" @click="storemanager_login">Store Manager Login</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      signup() {
        this.$router.push({ name: 'Signup' });
      },
      login() {
        this.$router.push({ name: 'Login' });
      },
      manager_login() {
        this.$router.push({ name: 'Login_Manager' });
      },
      storemanager_signup() {
        this.$router.push({ name: 'Storemanager_Signup' });
      },
      storemanager_login() {
        this.$router.push({ name: 'Storemanager_Login' });
      },
    },
  };
  </script>
  
  <style scoped>
    .center-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
  
    .header {
      text-align: center;
      margin-bottom: 20px;
    }
  
    .logo {
      color: #000; /* Black color for the logo */
      font-size: 24px;
    }
  
    .navbar {
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  
    .nav-buttons {
      display: flex;
      flex-direction: column;
    }
  
    .nav-buttons button {
      background-color: #2ecc71; /* Green color for the buttons */
      color: #fff;
      padding: 10px;
      margin: 10px 0;
      border: none;
      cursor: pointer;
      border-radius: 5px;
      transition: background-color 0.3s;
    }
  
    .nav-buttons button:hover {
      background-color: #27ae49; /* Darker green color for hover effect */
    }
  </style>
  
  <style>
    /* Global styles for the entire application */
    body {
      margin: 0;
      background-color: #3498db; /* Set the global background color */
      color: #fff;
      font-family: 'Arial', sans-serif; /* Set your preferred font-family */
    }
  </style>
  