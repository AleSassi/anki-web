<script setup lang="ts">
import TextField from '../components/TextField.vue'
import NavBar from '@/components/NavBar.vue';
import logoURL from '../assets/logo.svg'
import AuthController from '../controllers/auth_controller'
import { ref, computed } from "vue";
import router from "@/router/index";
import RoutingPath from "@/router/routing_path";
import HomeController from '@/controllers/home_controller';
import DeckList from '@/components/DeckList.vue';
import DeckEntry from '@/components/DeckEntry.vue';
import { onMounted } from 'vue';
import { CollectionData } from '@/model/collection_model';

const deckData = HomeController.getRef();
const deckList = ref<InstanceType<typeof DeckList> | null>(null);
const loading = ref(true);

onMounted(async () => {
    const res = await HomeController.getDecks();
    loading.value = false;
    if (deckList.value) {
        deckList.value.displayedData = res?.decks ?? [];
    }
})
</script>

<template>
    <NavBar active_index="0" />
    <div class="container-fluid">
        <div class="row">
            <div class="col-lg-6 col-md-12 order-md-3">
                <p v-if="loading" class="text-secondary text-center">Loading collection</p>
                <DeckList ref="deckList"/>
                <p class="text-center text-secondary pt-3" v-if="deckData && deckData.studiedTime > 0">It took {{ deckData?.studiedTime ?? 0 }} seconds to learn {{ deckData?.studiedCards ?? 0 }} cards today.</p>
                <p class="text-center text-secondary pt-3" v-if="!deckData || (deckData?.studiedTime ?? 0) == 0">You haven't studied anything today!</p>
            </div>

            <div class="col-md-1 order-md-1 d-none d-lg-block">
            </div>
            <div class="col-md-2 order-md-2 d-none d-lg-block">
            </div>

            <div class="col-md-3 mt-1 order-md-4">
            </div>
        </div>
    </div>
</template>

<style scoped>
#form-container {
    height: 100%;
}
</style>