<template>
  <div class="uk-height-viewport uk-width-viewport uk-cover-container uk-background-secondary">
    <transition name="None">
        <router-view></router-view>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'auth',
  data() {
    return {
      transitionName: null
    }
  },
  watch: {
      '$route' (to, from) {
        if (to.name == 'register' && from.name == 'login') {
          this.transitionName = 'slide-left'
        } else if (to.name == 'login' && from.name == 'register') {
          this.transitionName = 'slide-right'
        } else {
          this.transitionName = null
        }
      }
  }
}
</script>

<style scope>
/* Enter and leave animations can use different */
/* durations and timing functions.              */
.slide-left-enter-active, .slide-left-leave-active {
  transition: all 3s ease;
}

.slide-right-enter-active, .slide-right-leave-active {
  transition: all 3s ease;
}

.slide-left-leave-to {
  transform: translateX(-100%) ;
}

.slide-left-enter-to {
  transform: translateX(100%) ;
}

.slide-right-leave-to {
  transform: translateX(100%);
}

.slide-right-enter-to {
  transform: translateX(-100%);
}

.fade-enter-active, .fade-leave-active {
  transition: all 1s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.fade-enter-to, .fade-leave {
  opacity: 1;
}

</style>
