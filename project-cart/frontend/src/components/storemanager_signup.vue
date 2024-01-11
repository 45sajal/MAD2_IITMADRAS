<!-- <template>
    mate!
</template> -->

<!-- <template>
    <div>
      <h2>Store Manager Signup</h2>
      <form @submit.prevent="submitSignup">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="signupData.name" required>
  
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="signupData.email" required>

        <label for="password">Password:</label>
        <input type="password" id="password" v-model="signupData.password" required>
  
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template> -->

  <template>
    <div>
      <h2 class="text-center">Store Manager Signup</h2>
      <form @submit.prevent="submitSignup" class="signup-form">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="signupData.name" class="form-control" required>
        </div>
  
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="signupData.email" class="form-control" required>
        </div>
  
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="signupData.password" class="form-control" required>
        </div>
  
        <button type="submit" class="btn btn-primary">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        signupData: {
          name: "",
          email: "",
          password:""
        },
      };
    },
    methods: {
      submitSignup() {
        axios.post("http://localhost:5000/store-manager-request", this.signupData)
          .then(response => {
            console.log(response.data.message);
            this.$router.push('/');
           
          })
          .catch(error => {
            console.error("Error signing up store manager:", error);
          });
      },
    },
  };
  </script>

<style scoped>
.text-center {
  text-align: center;
}

.signup-form {
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
  background-color: #044614;
}
</style>
  