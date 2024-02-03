<template>
    <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom bg-body">
        <div class="col-md-3 mb-2 mb-md-0">
        </div>

        <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
            <li><a :href="RoutingPath.HOME" :class='getStyle(0)'>Decks</a></li>
            <li><a :href="RoutingPath.HOME" :class='getStyle(1)'>Add</a></li>
            <li><a :href="RoutingPath.HOME" :class='getStyle(2)'>Browse</a></li>
            <li><a :href="RoutingPath.HOME" :class='getStyle(3)'>Stats</a></li>
        </ul>

        <div class="col-md-3 text-end">
            <button type="button" class="btn btn-outline-primary me-2">Logout</button>
        </div>
    </header>
</template>

<script setup lang="ts">
import logo from '@/assets/images/logo_dark.svg';
import { useRouter } from 'vue-router';
import RoutingPath from '@/router/routing_path';
import AuthController from '@/controllers/auth_controller';
import { onMounted, ref, watch } from 'vue';
import { computed } from 'vue';

interface Props {
    active_index: string;
}

const props = defineProps<Props>();
const router = useRouter();
let user = AuthController.getRef();
let isAuth = ref(false);

onMounted(() => {
    isAuth.value = AuthController.isAuthenticated.value;
});

watch(user, (val) => {
    isAuth.value = AuthController.isAuthenticated.value;
});

function getStyle(idx: number): string {
    return "nav-link px-2" + (parseInt(props.active_index) == idx ? " link-secondary" : "")
}
</script>

<style scoped>
.bg-nav-bar {
    background-color: #1E2952;
}
</style>