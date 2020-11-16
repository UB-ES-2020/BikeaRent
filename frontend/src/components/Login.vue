<style>
  h1 {
    text-align: center;
    width: 100%;
  }
  div.form-label-group1 {
    margin-top: 1%;
    align-content: center;
    text-align: center;
    width: 100%;
    display: inline-block;
  }
  div.row2{
    width: 30%;
    display: inline-block;
  }
</style>
/* eslint-disable */
<template>
  <div id="app" >
      <div class="container" style="margin-bottom: 3%">
        <h1 style="margin-bottom: 2%; font-weight: bold">Sign In</h1>
        <div class="form-label-group1">
           <div class="row1">
             <label for="inputUsername" style="font-weight: bold">Username</label>
           </div>
           <div class="row2">
              <input type="username" id="inputUsername" class="form-control"
              placeholder="Username" required v-model="username"/>
           </div>
         </div>
         <div class="form-label-group1">
            <div class="row1">
             <label for="inputPassword" style="font-weight: bold">Password</label>
           </div>
           <div class="row2">
              <input type="password" id="inputPassword" class="form-control"
            placeholder="Password" required v-model="password" style="margin-bottom: 5%"/>
           </div>
         </div>
         <div class="form-label-group1">
           <div class="row2">
              <button type="button" class="btn btn-primary btn-lg btn-block" @click="checkLogin" style="float: right;">Sign In</button>
              <button type="button" class="btn btn-success btn-lg btn-block" @click="clearLogin" style="float: right">Create Account</button>
           </div>
        </div>
        <div>
            <b-modal id="bv-modal" hide-footer>
              <template v-slot:modal-title>
                <h4 style="text-align: center">Create Account</h4>
              </template>
              <div class="d-block">
                <b-form @submit="onSubmit" @reset="onReset">
                  <b-form-group id="input-group-3" label="Name:" label-for="input-1">
                    <b-form-input
                      id="input-1"
                      v-model="form.name"
                      required
                      placeholder="Enter your name"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="input-group-4" label="Surame:" label-for="input-2">
                    <b-form-input
                      id="input-2"
                      v-model="form.surname"
                      required
                      placeholder="Enter your surname"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="input-group-5" label="Mail:" label-for="input-3">
                    <b-form-input
                      id="input-3"
                      v-model="form.mail"
                      required
                      placeholder="Enter your mail"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="input-group-6" label="Username:" label-for="input-4">
                    <b-form-input
                      id="input-4"
                      v-model="form.usernameR"
                      required
                      placeholder="Enter your username"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="input-group-7" label="Password:" label-for="input-5">
                    <b-form-input
                      id="input-5"
                      v-model="form.passwordR"
                      required
                      placeholder="Enter your username"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="input-group-8" label="DNI:" label-for="input-6">
                    <b-form-input
                      id="input-6"
                      v-model="form.dni"
                      required
                      placeholder="Enter your DNI"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="input-group-9" label="DNI caducity:" label-for="input-7">
                    <b-form-input
                      id="input-7"
                      v-model="form.dni_caducity"
                      required
                      placeholder="Enter your Caducity DNI date"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="input-group-10" label="Credit Card:" label-for="input-8">
                    <b-form-input
                      id="input-8"
                      v-model="form.credit_card"
                      required
                      placeholder="Enter your credit card number"
                      >
                    </b-form-input>
                  </b-form-group>
                  <b-button type="submit" variant="primary" >Submit</b-button>
                  <b-button type="reset" variant="danger">Reset</b-button>
                </b-form>
              </div>
            </b-modal>
         </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      /* eslint-disable */
      user: {
        id: 0,
        token: null,
        username: '',
        type: 0,
        money_available: 0
      },
      form: {
        name: '',
        surname: '',
        mail: '',
        usernameR: '',
        passwordR: '',
        dni: '',
        licence_caducity: '',
        credit_card: '',
        type: 0
      }
    }
  },
  methods: {
    clearLogin () {
      this.username = ''
      this.password = ''
      this.form.name = ''
      this.form.surname = ''
      this.form.mail = ''
      this.form.usernameR = ''
      this.form.passwordR = ''
      this.form.dni = ''
      this.form.dni_caducity = ''
      this.form.credit_card = ''
      this.$bvModal.show('bv-modal')
    },
    checkLogin () {
      const parameters = {
        username: this.username,
        password: this.password
      }
      if (parameters.username === '' || parameters.password === '') {
        alert('Empty fields! Please try again.')
      } else {
        const path = 'https://bike-a-rent.herokuapp.com/login'
        axios.post(path, parameters)
          .then((res) => {
            this.user = res.data.user//this.token = res.data.token
            this.getAccount()
            alert('Log In Succesfully')
            this.$router.replace({
              path: '/home',
              query: {
                username: this.user.username,
                money: this.user.money_available,
                token: this.user.token,
                type: this.user.type
              }
            })
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error)
            alert('Username or Password incorrect')
          })
      }
    },
    getAccount () {
      const path = 'https://bike-a-rent.herokuapp.com/account' + this.user.id
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
    onSubmit () {
      this.$bvModal.hide('bv-modal')
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
          alert('Sign Up Successful! New account created!')
        })
        .catch((error) => {
          console.error(error)
          alert('Could not create the account!')
          alert(error)
        })
    },
    onReset () {
      this.form.name = ''
      this.form.surname = ''
      this.form.mail = ''
      this.form.usernameR = ''
      this.form.passwordR = ''
      this.form.dni = ''
      this.form.licence_caducity = ''
      this.form.credit_card = ''
    }
  }
}
</script>
