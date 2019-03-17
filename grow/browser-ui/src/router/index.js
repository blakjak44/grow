import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: 'home',
      redirect: { name: 'auth' }
    },
    {
      path: "/auth",
      name: 'auth',
      component: () => import("../views/Auth"),
      redirect: { name: 'login' },
      children: [
        {
          path: "login",
          name: 'login',
          component: () => import("../views/Login"),
        },
        {
          path: "register",
          name: 'register',
          component: () => import("../views/Register"),
        }
      ]
    },
    {
      path: "/dashboard/:user_id",
      name: 'dashboard',
      component: () => import("../views/Dashboard"),
      children: [
      ]
    }
  ]
});
