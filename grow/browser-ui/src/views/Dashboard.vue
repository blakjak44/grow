<template>
  <div class="uk-height-viewport uk-width-viewport uk-background-secondary">

    <!-- MEDIUM+ HEADER -->
    <nav class="uk-visible@s uk-navbar-container uk-navbar-transparent" uk-navbar>
      <div class="uk-navbar-left">
        <ul class="uk-navbar-nav">
          <li><a href="#">{{ currentUser.username }}</a></li>
        </ul>
      </div>
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav">
          <li><a href="" @:click.prevent="logout">Logout</a></li>
        </ul>
      </div>
    </nav>
    <!-- /MEDIUM+ HEADER -->

    <!-- SMALL HEADER -->
    <nav class="uk-hidden@s uk-navbar-container uk-navbar-transparent" uk-navbar>
      <div class="uk-navbar-left">
        <ul class="uk-navbar-nav uk-nav-primary">
          <li><a href="#left-bar" uk-icon="icon: menu; ratio: 2" uk-toggle></a></li>
        </ul>
      </div>
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav uk-nav uk-nav-primary">
          <li><a href="" @:click.prevent="logout">Logout</a></li>
        </ul>
      </div>
    </nav>
    <!-- /SMALL HEADER -->

    <!-- LEFT BAR -->
    <div class="uk-width-medium uk-visible@s">
      <div class="uk-container uk-padding-small">
        <ul class="uk-nav uk-nav-default">
          <li> <a href="">
              <span class="uk-margin-small-right" uk-icon="icon: thumbnails; ratio: 1.25"></span>
              Overview
            </a>
          </li>
          <li> <a href="">
              <span class="uk-margin-small-right" uk-icon="icon: history; ratio: 1.25"></span>
              History
            </a>
          </li>
          <li> <a href="">
              <span class="uk-margin-small-right" uk-icon="icon: cog; ratio: 1.25"></span>
              Configuration
            </a>
          </li>
        </ul>
      </div>
    </div>
    <!-- /LEFT BAR -->

    <!-- SMALL LEFT BAR -->
    <div id="left-bar" uk-offcanvas="overlay: true">
      <div class="uk-offcanvas-bar">
        <div class="uk-container uk-margin-small">
          <ul class="uk-nav uk-nav-primary">
            <li> <a href="">
                <span class="uk-margin-small-right" uk-icon="icon: thumbnails; ratio: 1.5"></span>
                Overview
              </a>
            </li>
            <li> <a href="">
                <span class="uk-margin-small-right" uk-icon="icon: history; ratio: 1.5"></span>
                History
              </a>
            </li>
            <li> <a href="">
                <span class="uk-margin-small-right" uk-icon="icon: cog; ratio: 1.5"></span>
                Configuration
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- /SMALL LEFT BAR -->

    <!-- LOADED CONTENT -->
    <router-view></router-view>
    <!-- /LOADED CONTENT -->
  </div>
</template>


<script>
import { mapGetters } from 'vuex'
import { LOGOUT } from "../store/actions.type";

export default {
  methods: {
    logout: function() {
      this.$store.dispatch( LOGOUT )
      .then(() => { this.$router.push({name: 'login'}) })
    }
  },
  computed: {
    ...mapGetters([
      'currentUser'
    ])
  }
}

</script>

<style scoped>
</style>
