import ApiService from "../common/api.service";
import { ADD_WIFI, SET_WIFI, SWITCH_AP, REBOOT } from "./actions.type";
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
  [SET_WIFI](context, ssid) {
    return new Promise(( resolve, reject ) => {
      ApiService.post("prov/set", ssid)
        .then(({ data })  => {
          resolve(data);
        })
        .catch(({ response }) => {
          debugger
          reject(response);
        });
    });
  },
  [SWITCH_AP](context, active) {
    return new Promise(( resolve, reject ) => {
      ApiService.post("prov/switch", { active })
        .then(({ data })  => {
          resolve(data);
        })
        .catch(({ response }) => {
          reject(response);
        });
    });
  },
  [REBOOT]() {
    return new Promise(( resolve, reject ) => {
      ApiService.get("prov/reboot")
        .then(({ data }) => {
          resolve(data);
        })
        .catch(({ response }) => {
          reject(response);
        })
    });
  }
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
