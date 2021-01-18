<template>
  <div id="app">
    <div id="space"></div>
    <img alt="Vue logo" id="logo" src="./assets/logo.png">
    <HelloWorld id="text" msg="Coming Soon."/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#logo{
    width:40%;
  }

@media only screen and (max-width: 650px) {
  #text{
    font-size: 12px;
  }
  #logo{
    width:80%;
  }
  #space {
  padding-top: 120px;
}
}

#app {
  font-family: Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #0f0f0f;
  margin-top: 60px;
  font-size: 14px;
}


</style>
