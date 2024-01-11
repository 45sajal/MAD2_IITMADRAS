<template>
  <div class="user-page-container">
    <h1>Welcome to the user page, mate.</h1>

    <div class="button-section">
      <button @click="MyCart">Go to cart</button>
      <button @click="Logout">Logout</button>
    </div>

    <h2>Sections</h2>
    <ul>
      <li v-for="section in sections" :key="section.section_id">
        <router-link :to="'/section/' + section.section_id + '/' + username + '/products'">
          {{ section.section_name }}
        </router-link>
        <router-view />
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'axios';
export default {
  data() {
    return {
      itemName: '',
      sections: [],
      username:''
    };
  },
  mounted() {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
      console.error("Access token not found.");
     
      return;
    }
    
    this.fetchUserData(accessToken)
  },
  methods: {
    MyCart(){
          this.$router.push({name:'Cart'})
    },
    Logout(){
      const token = localStorage.getItem('access_token');

      axios.post('http://localhost:5000/logout', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          
          this.$router.push('/');
          
        })
        .catch(error => {
          
        });
    },
    async fetchUserData(accessToken) {
      try {
        const response = await axios.get("http://127.0.0.1:5000/user_after_login_section", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.username = response.data.username;
        this.sections = response.data.sections;
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
  },
}
</script>


<style scoped>
.user-page-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  color: yellow
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.button-section {
  background-color: #3498db;
  color: white;
  padding: 10px;
  margin-right: 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color:green;
}

ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
}

router-link {
  text-decoration: none;
  color:black;
  font-weight: bold;
}

router-link:hover {
  text-decoration: underline;
}
</style>

