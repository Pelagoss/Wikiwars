<template>
  <router-view>
  </router-view>
</template>


<script>
import {emitter} from "./utils/index.js";
import {userStore} from "./store/index.js";

emitter.$on('unAuthorized', (data) => {
    console.log(userStore);
    userStore().logout();
});

export default {
    name: 'App'
};

</script>

<style lang="scss" scoped>
</style>