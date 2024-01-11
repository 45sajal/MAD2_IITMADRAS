

<template>
  <div class="container mt-5">
    <h2>List of all Sections</h2>
    <table class="table">
      <thead>
        <tr>
          <th>SNo</th>
          <th>Section_Name</th>
          <th>Section_Description</th>
          <th>Update_Section</th>
          <th>Delete_Section</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(section, index) in sections" :key="section.id">
          <td>{{ section.id }}</td>
          <td>{{ section.name }}</td>
          <td>{{ section.description }}</td>
          <td>
            <form @submit.prevent="updateSection(section.id, index)" method="post" class="update-form">
              <div class="form-group">
                <label for="section_name">Section Name:</label>
                <input type="text" class="form-control" v-model="sectionFormData[index].name" required>
              </div>

              <div class="form-group">
                <label for="section_description">Section Description:</label>
                <input type="text" class="form-control" v-model="sectionFormData[index].description" required>
              </div>

              <button type="submit" class="btn btn-primary">Update Section</button>
            </form>
          </td>
          <td>
            <button @click="deleteSection(section.id)" class="btn btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import { isAuthenticated } from '@/router';

export default {
  data() {
    return {
      sections: [],
      sectionFormData: [],
    };
  },
  mounted() {
    axios.get('http://127.0.0.1:5000/view_section')
      .then((response) => {
        this.sections = response.data;
        this.sectionFormData = this.sections.map(section => ({
          name: '',
          description:'',
        }));
        isAuthenticated.value = true;
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  },
  methods: {
    deleteSection(sectionId) {
      axios.delete(`http://127.0.0.1:5000/view_section/${sectionId}/delete`)
        .then(response => {
          console.log(response.data.message);
          this.$router.push('/manager_after_login');
        })
        .catch(error => {
          console.error(error.response.data.error);
        });
    },
    async updateSection(sectionId, index) {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/view_section/${sectionId}/update`, {
          section_name: this.sectionFormData[index].name,
          section_description: this.sectionFormData[index].description,
        });
        console.log(response.data);

        this.$router.push('/manager_after_login');
      } catch (error) {
        console.error(error);
      }
    },
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

.table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #dee2e6;
  padding: 8px;
  text-align: left;
}

.btn {
  padding: 8px;
  margin: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: green;
  color: white;
}

.btn-primary:hover {
  background-color: #06650b;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

.update-form {
  margin-top: 10px;
}
</style>