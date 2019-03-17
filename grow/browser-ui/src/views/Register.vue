<template>
  <div id="register" class="uk-flex uk-flex-center uk-flex-middle uk-flex-column uk-height-viewport uk-light uk-position-relative uk-position-z-index">
    <h1 class="uk-heading">Register</h1>
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
            <div v-if="formIncomplete">
              <span v-if="!textInUserField" class="uk-text-danger">Username is required.</span>
            </div>
          </div>
          <div class="uk-margin">
            <div class="uk-inline uk-width-1-1">
              <span class="uk-form-icon uk-form-icon-flip" uk-icon="icon: mail"></span>
              <input
                class="uk-input uk-border-rounded"
                type="text"
                v-model="email"
                placeholder="Email"
              />
            </div>
            <div v-if="formIncomplete">
              <span v-if="!textInEmailField" class="uk-text-danger">Email is required.</span>
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
                autocomplete="new-password"
              />
            </div>
            <div v-if="formIncomplete">
              <span v-if="!textInPassField" class="uk-text-danger">Password is required.</span>
            </div>
          </div>
          <div class="uk-margin">
            <div class="uk-inline uk-width-1-1">
              <input
                class="uk-input uk-border-rounded"
                type="password"
                v-model="passwordRepeat"
                placeholder="Confirm Password"
              />
            </div>
            <div v-if="textInBothPassFields">
              <span v-if="passwordsMatch" class="uk-text-success">Passwords match.</span>
              <span v-else class="uk-text-danger">Passwords do not mach.</span>
            </div>
          </div>
          <div class="uk-margin">
            <button class="uk-button uk-button-primary uk-border-rounded uk-width-1-1">Submit</button>
          </div>
        </fieldset>
      </form>
      <div class="uk-flex uk-flex-center uk-flex-middle">
        <p>Already registered?  <router-link to="/">Sign In</router-link></p>
      </div>
    </div>
  </div>
</template>


<script>
import UIkit from 'uikit';

import { REGISTER } from "@/store/actions.type";

export default {
  name: "register",
  data() {
    return {
      username: '',
      email: '',
      password: '',
      passwordRepeat: '',
      formIncomplete: false
    };
  },
  computed: {
    textInUserField: function() { return this.username != '' },
    textInEmailField: function() { return this.email != '' },
    textInPassField: function() { return this.password != '' },
    textInBothPassFields: function() { return this.password != '' && this.passwordRepeat != '' },
    passwordsMatch: function() { return this.password === this.passwordRepeat }
  },
  methods: {
    onSubmit() {
      this.formIncomplete = false;
      if ( !this.textInUserField ) {
        this.formIncomplete = true
      }
      if ( !this.textInEmailField ) {
        this.formIncomplete = true
      }
      if ( !this.textInPassField ) {
        this.formIncomplete = true
      }
      if ( this.formIncomplete ) { return }
      if ( this.passwordsMatch ) {
        let username = this.username;
        let password = this.password;
        let email = this.email;
        this.$store
          .dispatch( REGISTER, { username, password, email })
          .then( data => {
            UIkit.notification(data.message, {status:'success'})
            setTimeout( () => {
              this.$router.push({ path: `/dashboard/${data.user.user_id}` })
            }, 2000)
          })
          .catch( response => {
            response.data.errors.forEach( error => {
              UIkit.notification(error, {status:'danger'})
            })
          })
      }
    }
  }
};
</script>
