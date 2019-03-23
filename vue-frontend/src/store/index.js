import Vue from "vue";
import Vuex from "vuex";

import auth from "./auth.module";
import prov from "./prov.module";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    prov
  }
});
