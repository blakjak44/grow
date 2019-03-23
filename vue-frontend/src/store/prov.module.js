import ApiService from "../common/api.service";
import { ADD_WIFI, SET_WIFI } from "./actions.type";
import { SET_PROV } from "./mutations.type";

const state = {
  wifiSSID: {},
  isProvisioned: false
};

const getters = {
  currentSSID(state) {
    return state.wifiSSID;
  },
  isProvisioned(state) {
    return state.isProvisioned;
  }
};

const actions = {
  [ADD_WIFI](context, credentials) {
    return new Promise(( resolve, reject ) => {
      ApiService.post("prov/add", { credentials })
        .then(({ data })  => {
          resolve(data);
        })
        .catch(({ response }) => {
          reject(response);
        });
    });
  },
  [SET_WIFI]() {
    return new Promise(( resolve, reject ) => {
      ApiService.post("prov/set")
        .then(({ data })  => {
          resolve(data);
        })
        .catch(({ response }) => {
          reject(response);
        });
    });
  },
}

const mutations = {
  [SET_PROV](state, ssid) {
    state.isProvisioned = true;
    state.wifiSSID= ssid;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
