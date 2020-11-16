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
</style>

<template>
<div id="app">
  <div v-if="!navigation & !bikeAdding & !addEmpl">
    <nav class="navbar navbar-dark">
      <h2 style="color: #d3d9df">BaikaRent</h2>
      <div>
        <h6 style="color: #d3d9df">{{this.user.username}}</h6>
        <h6 style="color: #d3d9df">{{this.user.money_available}} €</h6>
      </div>
    </nav>
    <div v-if="user.type = 1" >
      <button style="position: absolute; right: 0%" class="btn btn-warning"  @click="bikeAdding=true">Add Bike</button>
    </div>
    <div v-if="user.type = 3" >
      <button type="button" class="btn btn-warning" @click="addEmpl=true" style="position: absolute; right: 10%">Add Employee</button>
    </div>
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
        <button class="btn btn-primary"  @click="showInfo(bike)">Info Bike</button>
        <button class="btn btn-warning"  @click="takeBike(bike)">Take Bike</button>
      </tbody>
    </table>
  </div>
  <div v-if="navigation">
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
  <div v-if="addEmpl">
    <h3> Add a new employee</h3>
    <b-card style="width:250px; margin:auto">
      <button class="btn btn-outline-dark btn-sm" style="margin-block-end: 10px; position:absolute;top:0;right:0;" @click="addEmpl=false">Close</button>
      <b-form-group id="input-group-20" label="Name:" label-for="input-20">
        <b-form-input
          id="input-20"
          v-model="form.name"
          required
          placeholder="Enter employee's name"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-21" label="Surame:" label-for="input-21">
        <b-form-input
          id="input-21"
          v-model="form.surname"
          required
          placeholder="Enter employee's surname"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-22" label="Mail:" label-for="input-22">
        <b-form-input
          id="input-22"
          v-model="form.mail"
          required
          placeholder="Enter the mail"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-23" label="Username:" label-for="input-23">
        <b-form-input
          id="input-23"
          v-model="form.usernameR"
          required
          placeholder="Enter the username"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-24" label="Password:" label-for="input-24">
        <b-form-input
          id="input-24"
          v-model="form.passwordR"
          required
          placeholder="Enter the password"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-25" label="DNI:" label-for="input-25">
        <b-form-input
          id="input-25"
          v-model="form.dni"
          required
          placeholder="Enter employee's DNI"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-26" label="TYPE(1 = Suport 2=Technical):" label-for="input-26">
        <b-form-input
          id="input-25"
          v-model="form.type"
          required
          placeholder="Enter employee's Type"
          >
        </b-form-input>
      </b-form-group>
      <button class="btn btn-danger" @click="submitEmployee, addEmpl=false">Add employee</button>
    </b-card>
  </div>
  <div v-if="bikeAdding">
    <h3> Add a bike in the system</h3>
    <b-card style="width:250px; margin:auto">
      <button class="btn btn-outline-dark btn-sm" style="margin-block-end: 10px; position:absolute;top:0;right:0;" @click="bikeAdding=false">Close</button>
      <b-form-group id="input-group-3" label="Model:" label-for="input-1">
        <b-form-input
          id="input-1"
          v-model="bike.model"
          required
          placeholder="Enter the bike model"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-4" label="Charge:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="bike.charge"
          required
          placeholder="Enter the bike charge"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-5" label="Latitude:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="bike.latitude"
          required
          placeholder="Enter the bike latitude"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-6" label="Longitude:" label-for="input-4">
        <b-form-input
          id="input-4"
          v-model="bike.longitude"
          required
          placeholder="Enter the bike longitude"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-7" label="Plate:" label-for="input-5">
        <b-form-input
          id="input-5"
          v-model="bike.plate"
          required
          placeholder="Enter the bike plate"
          >
        </b-form-input>
      </b-form-group>
      <button class="btn btn-danger" @click="addBike, bikeAdding=false">Add this bike</button>
    </b-card>
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
        money_available: 69,
        type: 0 // 0=user, 1=support, 2=technical, 3=admin
      },
      form: {
        name: '',
        surname: '',
        mail: '',
        usernameR: '',
        passwordR: '',
        dni: '',
        licence_caducity: '01-01-2999',
        credit_card: '999999999',
        type: 1
      },
      bike: {
        model: '',
        active: false,
        charge: '',
        latitude: '',
        longitude: '',
        plate: ''
      },
      supportLogged: true,

      bikes: [
        {
          model: 'Vespa',
          active: false,
          charge: 90,
          latitude: 909.87,
          longitude: 789.09,
          plate: 'Ola Soy una PlaTe'
        }
      ],
      navigation: false,
      active: false,
      addEmpl: false,
      bikeAdding: false
    }
  },
  methods: {
    // GET bikes
    getBikes () {
      const path = 'https://bike-a-rent.herokuapp.com/bikes'
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
      const path = 'https://bike-a-rent.herokuapp.com/account/' + this.user.id
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
    submitEmployee () {
      const parameters = {
        name: this.form.name,
        surname: this.form.surname,
        mail: this.form.mail,
        usernameR: this.form.usernameR,
        passwordR: this.form.passwordR,
        dni: this.form.dni,
        licence_caducity: this.form.licence_caducity,
        credit_card: this.form.credit_card,
        type: this.form.type
      }
      const path = 'https://bike-a-rent.herokuapp.com/account'
      axios.post(path, parameters)
        .then((res) => {
          alert('New employee added!')
        })
        .catch((error) => {
          console.error(error)
          alert('Could not create the account!')
          alert(error)
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
      const path = 'https://bike-a-rent.herokuapp.com/rent'
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

      const path = 'https://bike-a-rent.herokuapp.com/rent'
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
    addBike () {
      const path = 'https://bike-a-rent.herokuapp.com/bike'
      const parameters = {
        model: this.bike.model,
        active: true,
        charge: this.bike.charge,
        latitude: this.bike.latitude,
        longitude: this.bike.longitude
      }
      axios.post(path, parameters, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          this.user = res.data.user
        })
        .catch((error) => {
          console.error(error)
        })
    },
    showInfo (bike) {
      this.bike = bike
      this.bike.$bvModal.show('info-modal')
    }
  },
  created () {
    this.getBikes()
    this.getAccount()
    this.user.username = this.$route.query.username
    this.user.money_available = this.$route.query.token
    this.user.token = this.$route.query.token
    this.user.type = this.$route.query.type
  }
}
</script>
