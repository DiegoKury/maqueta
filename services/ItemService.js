import axios from 'axios';

const API_URL = 'http://localhost:8000/items';

class ItemService {
  getItems() {
    console.log('Getting items...')
    return axios.get(API_URL);
  }
  addItem(item) {
    console.log('Adding item...');
    return axios.post(API_URL, item);
  }
}

export default new ItemService();
