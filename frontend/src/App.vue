<script setup lang="ts">
import { storeToRefs } from "pinia";
import { watch } from "vue";
import { RouterView, useRouter } from "vue-router";
import NavBar from "./components/NavBar.vue";
import RoutingPath from "./router/routing_path";
import AuthController from "@/controllers/auth_controller";

// Used to access the router
const router = useRouter();

const user = localStorage.getItem("user");
if (user) {
  AuthController.setUser(JSON.parse(user));
}
// Always watch if the user is logged in
// if not, redirect to login
watch(AuthController.getRef(), (val) => {
  if (!val) return router.replace(RoutingPath.AUTH);
});
</script>

<template>
  <v-app id="app_container" class="bg-body-tertiary">
    <RouterView>
    </RouterView>
  </v-app>
</template>

<style scoped>
#app_container {
  min-height: 100vh;
}
</style>