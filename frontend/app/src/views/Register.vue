<template>
    <div id="form">
        <b-form @submit="register">

            <b-form-group id="input-group-2" label="First Name:" label-for="input-2">
            <b-form-input
              id="input-2"
              v-model="first_name"
              required
              placeholder="Enter your first name"
            ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-3" label="Last Name:" label-for="input-3">
            <b-form-input
              id="input-3"
              v-model="last_name"
              required
              placeholder="Enter your last name"
            ></b-form-input>
          </b-form-group>

            <b-form-group
            id="input-group-1"
            label="Email address:"
            label-for="input-1"
            description="We'll never share your email with anyone else."
            >
            <b-form-input
              id="input-1"
              v-model="email"
              type="email"
              required
              placeholder="Enter email"
            ></b-form-input>
            </b-form-group>

            <b-form-group
            id="input-group-4"
            label="Login username:"
            label-for="input-4"
            >
            <b-form-input
              id="input-4"
              v-model="login"
              type="text"
              required
            ></b-form-input>
            </b-form-group>

            <b-form-group
            id="input-group-5"
            label="Password:"
            label-for="input-5"
            >
            <b-form-input
              id="input-5"
              v-model="password"
              type="password"
              required
            ></b-form-input>
            </b-form-group>


        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
        <router-link to="/login" class="btn btn-secondary"tag="button">Back to Login</router-link>
    </b-form>
    </div>
</template>

<script>
    import { registerUser } from '../utils/auth'
    export default {
        data() {
            return {
                first_name: '',
                last_name: '',
                email: '',
                login: '',
                password: ''
            }
        },

        methods: {
             async register(evt) {
                try {
                    evt.preventDefault()
                    var new_user = {first_name: this.first_name, last_name: this.last_name,
                                    login: this.login, email: this.email, password: this.password}
                    await registerUser(new_user)
                    this.$router.push('/')
                }
                catch (error){
                    alert(`Error: ${error}`)

                }
            }
        }
    }
</script>

<style>
    .input-group {
        margin: 1rem;
    }

    .input-group label {
        margin-right: 0.5rem;
    }

    #form {
        position: absolute;
        left: 50%;
    }
</style>