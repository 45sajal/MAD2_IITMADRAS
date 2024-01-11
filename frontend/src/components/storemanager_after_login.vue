<!-- <template>
    <div class="ADD_PRODUCT">
        <button v-on:click="Aproduct">Add a product.</button>
    </div>
    <div class="VIEW_PRODUCT">
        <button v-on:click="Vproduct">View all products.</button>
    </div>
    <div id="app">
    <button @click="downloadCSV">Download CSV</button>
  </div>
  <div class="welcome">
    <button v-on:click="Goback">Logout</button>
    </div>
</template> -->

<template>
    <div>
      <div class="button-container">
        <button @click="Aproduct" class="action-button_01">Add a product</button>
        <button @click="Vproduct" class="action-button_02">View all products</button>
        <button @click="downloadCSV" class="action-button_03">Download CSV</button>
      </div>
  
      <div class="welcome">
        <button @click="Goback">Logout</button>
      </div>
    </div>
  </template>
<script>
import axios from 'axios';
export default{
    methods:{
        Aproduct(){
            this.$router.push({name:'Add_Product'})
        },
        Vproduct(){
            this.$router.push({name:'View_Product'})
        },
        downloadCSV() {
      axios.get('http://localhost:5000/download_csv')  
        .then(response => {
          const csvContent = response.data;

          const encodedUri = encodeURI(`data:text/csv;charset=utf-8,${csvContent}`);
          const link = document.createElement('a');
          link.setAttribute('href', encodedUri);
          link.setAttribute('download', 'products.csv');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        })
        .catch(error => console.error('Error fetching CSV content:', error));
    },
    Goback(){
        const token = localStorage.getItem('access_token');
        axios.post('http://localhost:5000/logout_manager', {}, {
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
.button-container {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

.action-button_01 {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: red;
  color: white;
  border: none;
  border-radius: 5px;
}
.action-button_02 {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: rgb(158, 6, 158);
  color: white;
  border: none;
  border-radius: 5px;
}
.action-button_03 {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: green;
  color: white;
  border: none;
  border-radius: 5px;
}

.action-button_01:hover {
  background-color: rgb(105, 8, 8);
}
.action-button_02:hover {
  background-color: rgb(71, 2, 71);
}
.action-button_03:hover {
  background-color: rgb(4, 55, 4);
}
.welcome {
  text-align: center;
  margin-top: 20px;
}

.welcome button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 5px;
}

.welcome button:hover {
  background-color: #5a6268;
}
</style>