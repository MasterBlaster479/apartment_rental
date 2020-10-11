<template>
    <div id="form" class="align-middle">
        <b-form @submit="loginUser">

            <b-form-group
            id="input-group-1"
            label="Login username:"
            label-for="input-1"
            >
            <b-form-input
              id="input-1"
              v-model="login"
              type="text"
              required
            ></b-form-input>
            </b-form-group>

            <b-form-group
            id="input-group-2"
            label="Password:"
            label-for="input-2"
            >
            <b-form-input
              id="input-2"
              v-model="password"
              type="password"
              required
            ></b-form-input>
            </b-form-group>


        <b-button type="submit" variant="primary">Login</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
                or
        <router-link to="/register" class="btn btn-secondary"tag="button">Register</router-link>
    </b-form>

    </div>
</template>

<script>
    import { loginUser } from '../utils/auth'
    export default {
        name: 'login',
        data() {
            return {
                login: 'goran',
                password: '1234'
            }
        },
        methods: {
             async loginUser(evt) {
                try {
                    evt.preventDefault()
                    await loginUser(this.login, this.password)
                    this.$router.push('/calendars')
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
    #form{
        position: absolute;
        left: 50%;
    }
</style>