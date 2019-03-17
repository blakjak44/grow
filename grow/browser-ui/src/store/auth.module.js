import ApiService from "../common/api.service";
import {
  LOGIN,
  LOGOUT,
  REGISTER,
  CHECK_AUTH,
  UPDATE_USER
} from "./actions.type";
import { SET_AUTH, PURGE_AUTH } from "./mutations.type";

const state = {
  user: {},
  isAuthenticated: false
};

const getters = {
  currentUser(state) {
    return state.user;
  },
  isAuthenticated(state) {
    return state.isAuthenticated;
  }
};

const actions = {
  [LOGIN](context, credentials) {
    return new Promise(( resolve, reject ) => {
      ApiService.post("auth/login", { credentials })
        .then(({ data })  => {
          context.commit(SET_AUTH, data.user);
          resolve(data);
        })
        .catch(({ response }) => {
          //context.commit(SET_ERROR, response.data.error);
          reject(response);
        });
    });
  },
  [LOGOUT](context) {
    return new Promise(resolve => {
      ApiService.get("auth/logout")
      .then(({ data  }) => {
        context.commit(PURGE_AUTH);
        resolve(data)
      })
    })
  },
  [REGISTER](context, credentials) {
    return new Promise(( resolve, reject ) => {
      ApiService.post("auth/register", { credentials })
        .then(({ data  }) => {
          context.commit(SET_AUTH, data.user);
          resolve(data);
        })
        .catch(({ response }) => {
          //context.commit(SET_ERROR, response.data.error);
          reject(response);
        });
    });
  },
  [CHECK_AUTH](context) {
    return new Promise((resolve, reject) => {
      ApiService.post("auth/validate")
        .then(({ data }) => {
          context.commit(SET_AUTH, data.user);
          resolve(data)
        })
        .catch(({ response }) => {
          //context.commit(SET_ERROR, response.data.error);
          context.commit(PURGE_AUTH);
          reject(response)
        });
    });
  },
  [UPDATE_USER](context, payload) {
    const { email, username, password, image, bio } = payload;
    const user = {
      email,
      username,
      bio,
      image
    };
    if (password) {
      user.password = password;
    }

    return ApiService.put("user", user).then(({ data }) => {
      context.commit(SET_AUTH, data.user);
      return data;
    });
  }
};

const mutations = {
  //[SET_ERROR](state, error) {
  //  state.errors = error;
  //},
  //[CLEAR_ERROR](state) {
  //  state.errors = {};
  //},
  [SET_AUTH](state, user) {
    state.isAuthenticated = true;
    state.user = user;
    //state.errors = {};
  },
  [PURGE_AUTH](state) {
    state.isAuthenticated = false;
    state.user = {};
    //state.errors = {};
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
