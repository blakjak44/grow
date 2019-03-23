<template>
  <div id="login" class="uk-flex uk-flex-center uk-flex-middle uk-flex-column uk-height-viewport uk-light uk-position-relative uk-position-z-index">
    <h1 class="uk-heading">Login</h1>
    <div class="uk-width-medium uk-padding-small">
      <form v-on:submit.prevent="onSubmit()">
        <fieldset class="uk-fieldset">
          <div class="uk-margin">
            <div class="uk-inline uk-width-1-1">
              <span class="uk-form-icon uk-form-icon-flip" uk-icon="icon: user"></span>
              <input
                class="uk-input uk-border-rounded"
                type="text"
                v-model="username"
                placeholder="Username"
              />
            </div>
          </div>
          <div class="uk-margin">
            <div class="uk-inline uk-width-1-1">
              <span class="uk-form-icon uk-form-icon-flip" uk-icon="icon: lock"></span>
              <input
                class="uk-input uk-border-rounded"
                type="password"
                v-model="password"
                placeholder="Password"
              />
            </div>
          </div>
          <div class="uk-margin">
            <button class="uk-button uk-button-primary uk-border-rounded uk-width-1-1">Submit</button>
          </div>
        </fieldset>
      </form>
      <div class="uk-flex uk-flex-center uk-flex-middle">
        <p>Need an account?  <router-link to="/auth/register">Register</router-link></p>
      </div>
    </div>
  </div>
</template>


<script>
import UIkit from 'uikit';

import { LOGIN } from "../store/actions.type";

export default {
  name: "login",
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    onSubmit() {
      let username = this.username;
      let password = this.password;
      this.$store.dispatch(LOGIN, { username, password })
        .then( data => {
          if (data.device_provisioned) {
            this.$router.push({ path: `/dashboard/${data.user.user_id}` })
          } else {
            this.$router.push({ path: '/provision' })
          }
        })
        .catch( response => {
          response.data.errors.forEach( error => {
            UIkit.notification(error, {status:'danger'})
          })
        })
    }
  }
};
</script>
