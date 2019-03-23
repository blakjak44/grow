<template>
  <div class="uk-height-viewport uk-width-viewport uk-background-secondary">

    <!-- MEDIUM+ HEADER -->
    <nav id="header" class="uk-visible@s uk-navbar-container uk-navbar-transparent" uk-sticky uk-navbar>
      <div class="uk-navbar-left">
        <ul class="uk-navbar-nav">
          <li><a href="#">{{ currentUser.username }}</a></li>
        </ul>
      </div>
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav">
          <li><a href="" v-on:click.prevent="logout">Logout</a></li>
        </ul>
      </div>
    </nav>
    <!-- /MEDIUM+ HEADER -->

    <!-- SMALL HEADER -->
    <nav id="header-small" class="uk-hidden@s uk-navbar-container uk-navbar-transparent" uk-sticky uk-navbar>
      <div class="uk-navbar-left">
        <ul class="uk-navbar-nav uk-nav-primary">
          <li><a href="#left-bar-small" uk-icon="icon: menu; ratio: 2" uk-toggle></a></li>
        </ul>
      </div>
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav uk-nav uk-nav-primary">
          <li><a href="" v-on:click.prevent="logout">Logout</a></li>
        </ul>
      </div>
    </nav>
    <!-- /SMALL HEADER -->

    <!-- LEFT BAR -->
    <aside id="left-bar" class="uk-light uk-visible@s">
      <div class="bar-wrap"> 
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
    </aside>
    <!-- /LEFT BAR -->

    <!-- SMALL LEFT BAR -->
    <div id="left-bar-small" uk-offcanvas="overlay: true">
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

    <div id="right-col" class="uk-visible@s">
      <!-- LOADED CONTENT -->
      <router-view></router-view>
      <!-- /LOADED CONTENT -->
    </div>

    <div id="right-col-small" class="uk-hidden@s">
      <!-- LOADED CONTENT -->
      <router-view></router-view>
      <!-- /LOADED CONTENT -->
    </div>

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
  #header, #header-small {
    background-color: #202020;
  }

  #left-bar {
    position: fixed;
    left: 0;
    top:0;
    bottom:0;
    overflow-x: hidden;
    overflow-y: auto;
    background-color: #222222;
    width: 220px;
    z-index:1;
  }

  .bar-wrap {
    margin-top: 70px;
    padding: 2rem;
  }

  #right-col {
    margin-left: 220px;
  }
</style>
