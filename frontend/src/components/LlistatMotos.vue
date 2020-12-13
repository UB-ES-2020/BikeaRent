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
  <div v-if="!navigation & !active & !bikeAdding & !bikeUpdate & !addEmpl & !finReserva">
    <nav class="navbar navbar-dark">
      <h2 style="color: #d3d9df">BaikaRent</h2>
      <h4 v-if="user.type == 1" style="margin: 0; color: #9f40bf">Support account</h4>
      <h4 v-if="user.type == 2" style="color: #f6a90f">Technician account</h4>
      <h4 v-if="user.type == 3" style="color: #ff00ff">Admin account</h4>
      <button type="button" class="btn-sm btn-outline-light" style="position: absolute; right: 5%;" @click="logout" >Logout</button>
      <div>
        <div>
          <button class="btn btn-primary" style="position: absolute; right: 15%" @click="showInfoUser()">Info User</button>
          <button class="btn btn-success" style="position: absolute; right: 25%" @click="userUpdate=true">Edit User</button>
        </div>
        <h6 style="color: #d3d9df">{{this.user.username}}</h6>
        <h6 v-if="user.type == 0 || user.type == 3" style="color: #d3d9df">{{this.user.availableMoney}} €</h6>
      </div>
    </nav>
    <div v-if="user.type == 1" >
      <button style="position: absolute; right: 0%; background-color:#9f40bf; color:white" class="btn btn-outline-dark"  @click="bikeAdding=true">Add Bike</button>
    </div>
    <div v-if="user.type == 3" >
      <button type="button" class="btn btn-warning" @click="addEmpl=true" style="position: absolute; right: 10%; background-color: #ff00ff">Add Employee</button>
    </div>
    <table v-if="user.type == 1 || user.type == 2 || user.type == 3">
      <thead style="border-bottom: 5px solid #000;">
        <tr>
          <th>Bike model</th>
          <th>Localated</th>
        </tr>
      </thead>
      <tbody v-for="(bike) in bikes" :key="bike.id">
        <td>{{ bike.model }} </td>
        <td>{{ bike.longitude }} , {{ bike.latitude }} </td>
        <button class="btn btn-primary"  @click="showInfo(bike)">Info Bike</button>
        <button v-if="user.type != 1" class="btn btn-danger"  @click="takeBike(bike)">Take Bike</button>
        <button v-if="user.type == 1" style="background-color:#9f40bf; color:white" class="btn btn-outline-dark"  @click="bikeUpdate=true">Update Bike</button>
      </tbody>
    </table>
  </div>
  <div v-if="navigation">
    <h3>Go to {{this.bike.latitude}}, {{ this.bike.longitude }} to unlock your bike.</h3>
    <div> Once you ara next to the bike, press the Unlock button to start the renting</div>
    <br>
    <button class="btn btn-info" @click="navigation=false, showMap=true">Cancel</button>
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
          <h5>Model: {{ bike.model }}</h5>
          <hr>
          <h5 class="mt-2">Charge: {{ bike.charge }}</h5>
          <h5>Location: {{bike.latitude}},{{bike.longitude}}</h5>
          <h5 class="mt-2">Plate: {{bike.plate}}</h5>
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
          v-model="newUserForm.firstname"
          required
          placeholder="Enter employee's name"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-21" label="Surame:" label-for="input-21">
        <b-form-input
          id="input-21"
          v-model="newUserForm.surname"
          required
          placeholder="Enter employee's surname"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-22" label="Mail:" label-for="input-22">
        <b-form-input
          id="input-22"
          v-model="newUserForm.email"
          required
          placeholder="Enter the mail"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-23" label="Username:" label-for="input-23">
        <b-form-input
          id="input-23"
          v-model="newUserForm.username"
          required
          placeholder="Enter the username"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-24" label="Password:" label-for="input-24">
        <b-form-input
          id="input-24"
          v-model="newUserForm.password"
          required
          placeholder="Enter the password"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-25" label="DNI:" label-for="input-25">
        <b-form-input
          id="input-25"
          v-model="newUserForm.dni"
          required
          placeholder="Enter employee's DNI"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-27" label="Credit Card:" label-for="input-27">
        <b-form-input
          id="input-27"
          v-model="newUserForm.creditCard"
          required
          placeholder="Enter employee's Credit Card"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-26" label="TYPE(1 = Suport 2=Technical):" label-for="input-26">
        <b-form-input
          id="input-25"
          v-model="newUserForm.type"
          required
          placeholder="Enter employee's Type"
          >
        </b-form-input>
      </b-form-group>
      <button class="btn btn-danger" @click="submitEmployee">Add employee</button>
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
      <button class="btn btn-danger" @click="addBike">Add this bike</button>
    </b-card>
  </div>
  <div v-if="finReserva">
    <h3>Rent details</h3>
    <b-card style="width:250px; margin:auto">
      <h4>Total time: {{this.reserva.totalTimeUsed}}</h4>
      <h4>Total cost: {{this.reserva.price}}</h4>
      <button class="btn btn-success" @click="finReserva=false">OK</button>
      <h5>Enjoy your day!</h5>
    </b-card>
  </div>
  <div v-if="bikeUpdate">
    <h3> Update a bike in the system</h3>
    <b-card style="width:250px; margin:auto">
      <button class="btn btn-outline-dark btn-sm" style="margin-block-end: 10px; position:absolute;top:0;right:0;" @click="bikeUpdate=false">Close</button>
      <b-form-group id="input-group-8" label="Model:" label-for="input-8">
        <b-form-input
          id="input-8"
          v-model="bike.model"
          required
          placeholder="Enter the bike model"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-9" label="Charge:" label-for="input-9">
        <b-form-input
          id="input-9"
          v-model="bike.charge"
          required
          placeholder="Enter the bike charge"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-10" label="Latitude:" label-for="input-10">
        <b-form-input
          id="input-10"
          v-model="bike.latitude"
          required
          placeholder="Enter the bike latitude"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-11" label="Longitude:" label-for="input-11">
        <b-form-input
          id="input-11"
          v-model="bike.longitude"
          required
          placeholder="Enter the bike longitude"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-12" label="Plate:" label-for="input-12">
        <b-form-input
          id="input-12"
          v-model="bike.plate"
          required
          placeholder="Enter the bike plate"
          >
        </b-form-input>
      </b-form-group>
      <button class="btn btn-danger" @click="updateBike(bike), bikeUpdate=false">Update this bike</button>
    </b-card>
  </div>
  <div>
    <b-modal id="infoUser-modal" hide-footer>
      <template v-slot:modal-title>
        <h4 style="text-align: center">Info Usuari</h4>
      </template>
      <div class="d-block">
        <br>
          <h5>ID: {{ user.id }}</h5>
          <hr>
          <h5 class="mt-2">Name: {{ user.firstname }}</h5>
          <h5 class="mt-2">Lastname: {{ user.surname }}</h5>
          <h5 class="mt-2">Mail: {{ user.email }}</h5>
          <h5 class="mt-2">Username: {{ user.username }}</h5>
          <h5 class="mt-2">DNI: {{ user.dni }}</h5>
          <h5 class="mt-2">Data End Drive Permission: {{ user.dataEndDrivePermission }}</h5>
          <h5 class="mt-2">Credit Card: {{user.creditCard}}</h5>
          <h5 class="mt-2">Available Money: {{user.availableMoney}}</h5>
          <h5>Location: {{user.latitude}},{{user.longitude}}</h5>
      </div>
    </b-modal>
  </div>
  <div v-if="userUpdate">
    <h3> Update a user in the system</h3>
    <b-card style="width:250px; margin:auto">
      <button class="btn btn-outline-dark btn-sm" style="margin-block-end: 10px; position:absolute;top:0;right:0;" @click="userUpdate=false">Close</button>
      <b-form-group id="input-group-13" label="Name:" label-for="input-13">
        <b-form-input
          id="input-13"
          v-model="user.firstname"
          required
          placeholder="Enter your name"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-14" label="Lastname:" label-for="input-14">
        <b-form-input
          id="input-14"
          v-model="user.surname"
          required
          placeholder="Enter your lastname"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-15" label="Username:" label-for="input-15">
        <b-form-input
          id="input-15"
          v-model="user.username"
          required
          placeholder="Enter your username"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-16" label="Email:" label-for="input-16">
        <b-form-input
          id="input-16"
          v-model="user.email"
          required
          placeholder="Enter your email address"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-17" label="DNI:" label-for="input-17">
        <b-form-input
          id="input-17"
          v-model="user.dni"
          required
          placeholder="Enter your DNI"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-18" label="Data End Drive Permission:" label-for="input-18">
        <b-form-input
          id="input-18"
          v-model="user.dataEndDrivePermission"
          required
          placeholder="Enter the end data of your permission"
          >
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-19" label="Credit Card:" label-for="input-19">
        <b-form-input
          id="input-19"
          v-model="user.creditCard"
          required
          placeholder="Enter your credit card"
          >
        </b-form-input>
      </b-form-group>
      <button class="btn btn-danger" @click="updateUser(), userUpdate=false">Update this user</button>
    </b-card>
  </div>
  <div v-if="showMap">
    <div class="map-container">
      <gmap-map
        id="map"
        ref="map"
        :center="center"
        :zoom="13"
        map-type-id="roadmap"
        style="width:100%;  height: 600px;">
        <gmap-info-window
          :options="infoOptions"
          :position="infoPosition"
          :opened="infoOpened"
          @closeclick="infoOpened=false">
          <div>
            <p>Id: {{bike.id}}</p>
            <p>Plate: {{bike.plate}}</p>
            <p>Charge: {{bike.charge}}</p>
            <p>Model: {{bike.model}}</p>
            <button class="btn btn-danger"  @click="takeBike(bike)">Take Bike</button>
          </div>
        </gmap-info-window>
        <gmap-marker
          :key="bike.id"
          v-for="(bike) in bikes"
          :position="{lat: bike.latitude, lng: bike.longitude}"
          @click="toggleInfoWindow(bike)"
          :icon="markerOptions"
        ></gmap-marker>
       </gmap-map>
    </div>
  </div>
</div>

</template>

<script>
import axios from 'axios'
import * as VueGoogleMaps from 'vue2-google-maps'
import { mapState } from 'vuex'
export default {
  name: 'Map',
  data () {
    return {
      user: {
        id: 0,
        token: null,
        username: 'Albert',
        availableMoney: 69,
        type: 0 // 0=user, 1=support, 2=technical, 3=admin
      },
      newUserForm: {
        firstname: '',
        surname: '',
        email: '',
        username: '',
        password: '',
        dni: '',
        dataEndDrivePermission: 'XXX',
        creditCard: '',
        type: null
      },
      bike: {
        id: 0,
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
      reserva: {
        totalTimeUsed: 0,
        price: 0
      },
      navigation: false,
      active: false,
      addEmpl: false,
      bikeAdding: false,
      bikeUpdate: false,
      finReserva: false,
      userUpdate: false,
      map: null,
      showMap: true,
      markerOptions: {
        url: require('../assets/moto_red_64_background.png')
      },
      infoPosition: null,
      infoContent: '',
      infoOpened: false,
      currentMidx: null,
      infoOptions: {
        pixelOffset: {
          width: 0,
          height: -35
        }
      }
    }
  },
  computed: {
    ...mapState([
      'map'
    ]),
    mapStyle: function () {
      const h = document.body.clientHeight - 80
      return 'width: 100%; height: ' + h + 'px'
    },
    center: function () {
      return { lat: 41.38879, lng: 2.15899 }
    }
  },
  mounted () {
    this.initMap()
  },
  methods: {
    // GET bikes
    getBikes () {
      const path = 'https://bike-a-rent.herokuapp.com/bikes'
      axios.get(path)
        .then((res) => {
          this.bikes = []
          this.bikes = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    submitEmployee () {
      const parameters = {
        firstname: this.newUserForm.firstname,
        surname: this.newUserForm.surname,
        email: this.newUserForm.email,
        username: this.newUserForm.username,
        password: this.newUserForm.password,
        dni: this.newUserForm.dni,
        dataEndDrivePermission: this.newUserForm.dataEndDrivePermission,
        creditCard: this.newUserForm.creditCard,
        type: this.newUserForm.type,
        latitude: 0,
        longitude: 0
      }
      const path = 'https://bike-a-rent.herokuapp.com/account'
      axios.post(path, parameters)
        .then((res) => {
          alert('New employee added!')
          this.addEmpl = false
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
      this.showMap = false
      this.infoOpened = false
    },
    unlockBike () {
      const parameters = {
        userid: this.user.id,
        bikeid: this.bike.id
      }
      const path = 'https://bike-a-rent.herokuapp.com/rent'
      axios.post(path, parameters)
        .then((res) => {
          this.navigation = false
          this.active = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert(error)
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
          this.reserva.totalTimeUsed = res.data.totalTimeUsed
          this.reserva.price = res.data.price
          this.getAccount() // actualitzem diners user
          this.active = false
          this.finReserva = true
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
        longitude: this.bike.longitude,
        plate: this.bike.plate
      }
      axios.post(path, parameters)
        .then((res) => {
          alert('New bike created!')
          this.bikeAdding = false
          // this.created()
        })
        .catch((error) => {
          alert(error)
          console.error(error)
        })
    },
    showInfo (bike) {
      this.bike = bike
      this.$bvModal.show('info-modal')
    },
    getAccount () {
      const path = 'https://bike-a-rent.herokuapp.com/account/' + this.user.username
      axios.get(path)
        .then((res) => {
          this.user = res.data
          this.user.availableMoney = res.data.availableMoney
        })
        .catch((error) => {
          console.error(error)
        })
    },
    updateBike (bike) {
      const path = 'https://bike-a-rent.herokuapp.com/bike/' + this.bike.id
      const parameters = {
        model: this.bike.model,
        active: true,
        charge: this.bike.charge,
        latitude: this.bike.latitude,
        longitude: this.bike.longitude,
        plate: this.bike.plate
      }
      axios.put(path, parameters, {
        auth: {username: this.user.token}
      })
        .then(() => {
          alert('Bike updated')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getToUpdate (bike) {
      this.bikeUpdate = true
      document.getElementById('input-8').value = bike.model
      document.getElementById('input-9').value = bike.charge
      document.getElementById('input-10').value = bike.latitude
      document.getElementById('input-11').value = bike.longitude
      document.getElementById('input-12').value = bike.plate
    },
    showInfoUser () {
      this.$bvModal.show('infoUser-modal')
    },
    logout () {
      this.$router.replace({path: '/'})
    },
    updateUser () {
      const path = 'https://bike-a-rent.herokuapp.com/account/' + this.user.id
      const parameters = {
        firstname: this.user.firstname,
        surname: this.user.surname,
        username: this.user.username,
        email: this.user.email,
        dni: this.user.dni,
        dataEndDrivePermission: this.user.dataEndDrivePermission,
        creditCard: this.user.creditCard
      }
      axios.put(path, parameters, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          this.user = res.data.user
          alert('User updated')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getMap (callback) {
      function checkForMap () {
        if (this.map) callback(this.map)
        else setTimeout(checkForMap, 200)
      }
      checkForMap()
    },
    initMap () {
      VueGoogleMaps.loaded.then(() => {
        this.map = new VueGoogleMaps.gmapApi.maps.Map(document.getElementById('map'))
      })
    },
    toggleInfoWindow (bike) {
      this.infoPosition = {lat: bike.latitude, lng: bike.longitude}
      this.bike = bike
      this.infoOpened = true
    }
  },
  created () {
    this.getBikes()
    this.user.username = this.$route.query.username
    this.user.token = this.$route.query.token
    this.getAccount()
  }
}
</script>
