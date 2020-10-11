<template>
  <div id="app">
    <div id="nav" v-if="isLoggedIn()">
      <router-link to="/">Home</router-link> |
      <router-link to="/calendars">Calendars</router-link>
    </div>
    <div id="user" v-if="isLoggedIn()">
        <router-link to="/profile">{{ getUserName() }}</router-link>
        <br/>
        <b-button type="button" variant="primary" v-on:click="logOut">Log Out</b-button>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#user {
    padding: 25px;
    margin-top:-100px;
    float: right;
}
</style>
<script>
    import { isLoggedIn, getUserInfo, logoutUser } from './utils/auth'
    export default {
        methods: {
            isLoggedIn() {
                return isLoggedIn()
            },
            getUserName() {
                return getUserInfo()['identity']
            },
            logOut() {
                logoutUser()
                this.$router.push('/')

            }
        },
    }
</script>
