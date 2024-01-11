<!-- <template>
    <div>add section</div>
</template> -->

<!-- <template>
    <div class="container mt-5">
      <h1>Add Section</h1>
      <form @submit.prevent="createSection" class="mt-4">
        <div class="form-group">
          <label for="s_name">Section Name:</label>
          <input v-model="sectionName" type="text" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="s_description">Section Description:</label>
          <input v-model="sectionDescription" type="text" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Create Section</button>
      </form>
    </div>
  </template> -->

  
  <template>
    <div class="container mt-5">
      <h1 class="section-title">Add Section</h1>
      <form @submit.prevent="createSection" class="section-form mt-4">
        <div class="form-group">
          <label for="s_name" class="form-label">Section Name:</label>
          <input v-model="sectionName" type="text" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="s_description" class="form-label">Section Description:</label>
          <input v-model="sectionDescription" type="text" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Create Section</button>
      </form>
    </div>
  </template>

<script>
import axios from 'axios';
import { isAuthenticated } from '@/router';
export default {
  data() {
    return {
      sectionName: "",
      sectionDescription: "",
    };
  },
  methods: {
    createSection() {
      const formData = {
        s_name: this.sectionName,
        s_description: this.sectionDescription,
      };

      axios
        .post('http://127.0.0.1:5000/add_section', formData)
        .then((response) => {
          console.log(response.data.message);
          isAuthenticated.value = true;
          this.$router.push('/manager_after_login');
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.section-title {
  text-align: center;
  color: #333;
}

.section-form {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  padding: 10px;
  background-color: green;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: rgb(3, 68, 3);
}
</style>