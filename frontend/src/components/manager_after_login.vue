  <template>
    <div class="manager-page">
      <h1>Welcome to the manager page mate.</h1>
      
      <div class="button-section">
        <button v-on:click="Asection">Add a Section</button>
        <button v-on:click="Vsection">View all Sections</button>
      </div>
  
      <div id="app" class="request-container">
        <div v-for="request in storeManagerRequests" :key="request.id" class="request-item">
          {{ request.name }} - {{ request.email }}
          <button class="approval" @click="approveRequest(request.id)">Approve</button>
          <button class="denial" @click="denyRequest(request.id)">Deny</button>
        </div>
      </div>
  
      <div class="welcome">
        <button v-on:click="Goback">Logout</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default{
    data() {
      return {
        storeManagerRequests: [],
      };
    },
    mounted() {
      this.fetchStoreManagerRequests();
    },
    methods:{
        Asection(){
            this.$router.push({name:'Add_Section'})
        },
        Vsection(){
            this.$router.push({name:'View_Section'})   
        },
        fetchStoreManagerRequests() {
        axios.get("http://localhost:5000/store-manager-request")
          .then(response => {
            this.storeManagerRequests = response.data;
          })
          .catch(error => {
            console.error("Error fetching store manager requests:", error);
          });
      },
      approveRequest(id) {
        axios.post("http://localhost:5000/admin-approve", { id })
          .then(response => {
            console.log(response.data.message);
            this.fetchStoreManagerRequests();
          })
          .catch(error => {
            console.error("Error approving request:", error);
          });
      },
      denyRequest(id) {
        axios.post("http://localhost:5000/admin-deny", { id })
          .then(response => {
            console.log(response.data.message);
            this.fetchStoreManagerRequests();
          })
          .catch(error => {
            console.error("Error denying request:", error);
          });
      },
      Goback(){
        
        const token = localStorage.getItem('access_token');

      axios.post('http://localhost:5000/logout_admin', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          
          this.$router.push('/');
        })
        .catch(error => {
        });
      }
    }
  }
  </script>
  

  
  <style scoped>
  .manager-page {
    max-width: 800px;
    margin: auto;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    text-align: center;
    color: #333;
  }
  
  .button-section {
    margin-top: 20px;
    text-align: center;
  }
  
  button {
    padding: 10px;
    margin: 5px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .request-container {
    margin-top: 20px;
  }
  
  .request-item {
    border: 1px solid #dee2e6;
    border-radius: 4px;
    margin-bottom: 10px;
    padding: 10px;
    color:black
  }
  
  .welcome {
    text-align: center;
    margin-top: 20px;
  }
  
  .approval{
    background-color: green;
  }
  .denial{
    background-color: red;
  }
  .approval:hover{
    background-color: rgb(4, 61, 4);
  }
  .denial:hover{
    background-color: rgb(94, 6, 6);
  }
  .welcome button {
    padding: 10px;
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .welcome button:hover {
    background-color: #c82333;
  }
  </style>