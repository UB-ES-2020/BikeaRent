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
        <td>{{ bike.street }} </td>
        <button class="btn btn-warning"  @click="takeBike(bike)">Take Bike</button>
      </tbody>
    </table>
  </div>
  <div v-else>
    <h3>Go to {{this.bike.street}} to unlock your bike.</h3>
    <div> Once you ara next to the bike, press the Unlock button to start the renting</div>
    <br>
    <button class="btn btn-outline-danger" @click="unlockBike">Unlock Bike</button>
  </div>
  <div v-if="active">
    <h1>Time is running!!</h1>
    <div> Once you have stoped the bike, press the Lock button to end the renting</div>
    <button class="btn btn-danger" @click="lockBike">Lock </button>
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
        username: 'Pene',
        money_available: 69
      },
      bike: {
        id: 0,
        battery: 100,
        model: '',
        street: ''
      },
      bikes: [
        {
          id: 1,
          model: 'Honda',
          street: 'Ronda Universitat, 5'
        },
        {
          id: 2,
          model: 'Vespa',
          street: 'Plaça Catalunya'
        },
        {
          id: 3,
          model: 'Vespa con sidecar',
          street: 'Plaça Universitat'
        }
      ],
      navigation: false,
      active: false
    }
  },
  methods: {
    // GET bikes
    getBikes () {
      const path = `http://127.0.0.1:5000/bikes`
      axios.get(path)
        .then((res) => {
          this.bikes = res.data.bikes
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getAccount () {
      const path = `http://127.0.0.1:5000/account/${this.user.id}`
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
      const path = `http://127.0.0.1:5000/rent`
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
      const path = `http://127.0.0.1:5000/rent`
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
