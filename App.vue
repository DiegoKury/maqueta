<template>
  <v-app>
    <v-main>
      <v-container>
        <h1>Add New Item</h1>
        <v-form @submit.prevent="submitItem">
          <v-text-field
            v-model="newItem.name"
            label="Name"
            required
          ></v-text-field>
          <v-textarea
            v-model="newItem.description"
            label="Description"
            required
          ></v-textarea>
          <v-btn
            color="primary"
            type="submit"
          >
            Add Item
          </v-btn>
        </v-form>
        <v-data-table
          :headers="headers"
          :items="items"
          class="elevation-1"
        ></v-data-table>
        <br>
        <input type="file" @change="handleFileUpload"/>
        <v-btn @click="submitFile">Upload File</v-btn>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';
import ItemService from '@/services/ItemService';

export default {
  data() {
    return {
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Name', value: 'name' },
        { text: 'Description', value: 'description' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      items: [],
      newItem: { name: '', description: '' },
    };
  },
  mounted() {
    this.loadItems();
  },
  methods: {
    async loadItems() {
      try {
        const response = await ItemService.getItems();
        this.items = response.data;
      } catch (error) {
        console.error('Error loading items:', error);
      }
    },
    async submitItem() {
      try {
        const response = await ItemService.addItem(this.newItem);
        this.items.push(response.data);
        this.newItem = { name: '', description: '' };
      } catch (error) {
        console.error('Error adding item:', error);
      }
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
  async submitFile() {
    if (!this.file) return;
    let formData = new FormData();
    formData.append("file", this.file);
    
    try {
      await axios.post('http://localhost:8000/uploadfile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'access_token': 'test_value',
        }
      });
      // handle success
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  }
  },
};
</script>
