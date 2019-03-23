<template>
  <div id="app">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#222222"/>
      <router-view></router-view>
  </div>
</template>

<script>
  import UIkit from 'uikit';
  import Icons from 'uikit/dist/js/uikit-icons';

  UIkit.use(Icons);

  export default {
    name: 'app',
    components: {
    }
  }
</script>

<style lang="less">
  @import "../node_modules/uikit/src/less/uikit.less";
</style>
