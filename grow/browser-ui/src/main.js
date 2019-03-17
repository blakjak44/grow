import Vue from 'vue'
import App from './App.vue'
import router from "./router";
import store from "./store";

import ApiService from "./common/api.service";
import { CHECK_AUTH } from "./store/actions.type";

Vue.config.productionTip = false

ApiService.init();

const noAuthRoutes = ['auth', 'login', 'register']

// Ensure we checked auth before each page load.
router.beforeEach((to, from, next) => {
  if (noAuthRoutes.indexOf(to.name) > -1) {
    next()
  } else {
  //Promise.all([store.dispatch(CHECK_AUTH)]).then(next)
    store.dispatch( CHECK_AUTH )
    .then(next)
    .catch( () => { router.push({ name: 'home' }) })
  }
});

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
