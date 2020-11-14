<style>
  th, td {
    padding: 15px;
    text-align: center;
  }
  .navbar {
    z-index: 1;
    background-color: #333;
    position: fixed;
    top: 0;
    width: 100%;
  }
  .floated {
    float:left;
    margin-right:5px;
  }
</style>

<template>
  <div id="app">
    <div v-if="!navigation">
      <nav class="navbar navbar-dark">
        <h2 style="color: #d3d9df">BaikaRent</h2>
        <div>
          <h6 style="color: #d3d9df">{{this.user.username}}</h6>
          <h6 style="color: #d3d9df">{{this.user.money_available}} €</h6>
        </div>
      </nav>
      <table>
        <thead style="border-bottom: 5px solid #000;">
          <tr>
            <th>Bike model</th>
            <th>Localated</th>
          </tr>
        </thead>
        <tbody v-for="(bike) in bikes" :key="bike.id">
          <td>{{ bike.model }} </td>
          <td>{{ bike.latitude, bike.longitude }} </td>
          <button class="btn btn-warning"  @click="takeBike(bike)">Take Bike</button>
          <button class="btn btn-primary"  @click="showInfo(bike)">Info Bike</button>
        </tbody>
      </table>
    </div>
    <div v-else>
      <h3>Go to {{this.bike.latitude, this.bike.longitude}} to unlock your bike.</h3>
      <div> Once you ara next to the bike, press the Unlock button to start the renting</div>
      <br>
      <button class="btn btn-outline-danger" @click="unlockBike">Unlock Bike</button>
    </div>
    <div v-if="active">
      <h1>Time is running!!</h1>
      <div> Once you have stoped the bike, press the Lock button to end the renting</div>
      <button class="btn btn-danger" @click="lockBike">Lock </button>
    </div>
    <div>
      <b-modal id="info-modal" hide-footer>
        <template v-slot:modal-title>
            <h4 style="text-align: center">Info</h4>
          </template>
        <div class="d-block">
          <br>
            <h5>ID: {{ bike.id }}</h5>
            <h5>Model: {{ bike.model }}</h5>
            <hr>
            <h5 class="mt-2">Charge: {{ bike.charge }}</h5>
            <h5>Location: {{ bike.latitude, bike.longitude }}</h5>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      user: {
        id: 0,
        token: null,
        username: '',
        money_available: 69
      },
      bike: {
        id: 0,
        model: '',
        charge: 0,
        latitude: 0.0,
        longitude: 0.0
      },
      bikes: [],
      navigation: false,
      active: false
    }
  },
  methods: {
    // GET bikes
    getBikes () {
      const path = 'https://bikearent4.herokuapp.com/bikes'
      axios.get(path)
        .then((res) => {
          this.bikes = []
          this.bikes = res.data.bikes
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getAccount () {
      const path = 'https://bikearent4.herokuapp.com/account/' + this.user.id
      axios.get(path, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          this.user = res.data.user
        })
        .catch((error) => {
          console.error(error)
        })
    },
    // Take a bike
    takeBike (bike) {
      this.bike = bike
      this.navigation = true
    },
    unlockBike () {
      const parameters = {
        user_id: this.user.id,
        bike_id: this.bike.id
      }
      const path = 'https://bikearent4.herokuapp.com/rent'
      axios.post(path, parameters)
        .then((res) => {
          this.active = true
          // this.bikes.splice(this.bike.id, 1)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert('Sorry, you cannot take this bike. Try again')
        })
    },
    lockBike () {
      const parameters = {
        user_id: this.user.id,
        bike_id: this.bike.id
      }
      const path = 'https://bikearent4.herokuapp.com/rent'
      axios.put(path, parameters)
        .then((res) => {
          this.active = false
          this.navigation = false
          // actualitzem diners
          this.getAccount()
          // this.bikes.splice(this.bike.id, 1)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert('Sorry, you cannot take this bike. Try again')
        })
    },
    showInfo (bike) {
      this.bike.id = bike.id
      this.bike.model = bike.model
      this.bike.charge = bike.charge
      this.bike.latitude = bike.latitude
      this.bike.longitude = bike.longitude
      this.bike.$bvModal.show('info-modal')
    }
  },
  created () {
    this.getBikes()
    this.getAccount()
    this.user.username = this.$route.query.username
    this.user.money_available = this.$route.query.token
    this.user.token = this.$route.query.token
  }
}
</script>
