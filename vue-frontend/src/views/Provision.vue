<template>
  <div id='provision' class="uk-flex uk-flex-center uk-flex-middle uk-flex-column uk-height-viewport uk-light uk-position-relative uk-position-z-index">
    <h1 class="uk-heading">Provision Device</h1>
    <div class="uk-width-medium uk-padding-small">
      <form v-on:submit.prevent="onSubmit()">
        <fieldset class="uk-fieldset">
          <div class="uk-margin">
            <div class="uk-inline uk-width-1-1">
              <span class="uk-form-icon uk-form-icon-flip" uk-icon="icon: link"></span>
              <input
                class="uk-input uk-border-rounded"
                type="text"
                v-model="ssid"
                placeholder="SSID"
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
                autocomplete="new-password"
              />
            </div>
          </div>
          <div class="uk-margin">
            <button class="uk-button uk-button-primary uk-border-rounded uk-width-1-1">Submit</button>
          </div>
        </fieldset>
      </form>
      <div class="uk-flex uk-flex-center uk-flex-middle">
        <p>Please enter wifi network credentials.</p>
      </div>
    </div>
  </div>
</template>


<script>
import UIkit from 'uikit';

import { ADD_WIFI, SET_WIFI, REBOOT } from "../store/actions.type";

export default {
  name: "provision",
  data() {
    return {
      ssid: '',
      password: ''
    };
  },
  methods: {
    onSubmit() {
      let ssid = this.ssid;
      let password = this.password;
      this.$store.dispatch(ADD_WIFI, { ssid, password })
        .then( data => {
          UIkit.notification(data.message, { status:'success' })
          this.$store.dispatch(SET_WIFI).then( data => {
            UIkit.notification(data.message, { status:'success' });
            UIkit.notification(
              'Device will now reboot. Please connect to the new WiFi network.',
              { status:'success' }
            );
            this.$store.dispatch(REBOOT)
          })
        })
        .catch( response => {
          response.data.errors.forEach( error => {
            UIkit.notification(error, { status:'danger' })
          })
        })
    }
  }
};
</script>

<style scoped>
#provision {
  background-color: #2A2A2A;
}
</style>
