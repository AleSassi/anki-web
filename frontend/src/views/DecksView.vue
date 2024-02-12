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
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';

const deckData = HomeController.getRef();
const deckList = ref<InstanceType<typeof DeckList> | null>(null);
const loadingRef = ref(true);
const deckName = ref("");

onMounted(async () => {
    loadingRef.value = true;
    const res = await HomeController.getDecks();
    loadingRef.value = false;
    if (deckList.value) {
        deckList.value.displayedData = res?.decks ?? [];
    }
})

function onNavBarEvent(id: number) {
    if (id == 1) {
        onClickCreateDeck();
    }
}

function onClickCreateDeck() {
    deckName.value = "";
}

async function onCreateDeck() {
    loadingRef.value = true;
    const res = await HomeController.createDeck(deckName.value);
    if (res) {
        const refreshRes = await HomeController.getDecks();
        if (deckList.value) {
            deckList.value.displayedData = refreshRes?.decks ?? [];
        }
    }
    loadingRef.value = false;
}
</script>

<template>
    <NavBar active_index="0" @optionSelected="(option) => onNavBarEvent(option)"/>
    <loading v-model:active="loadingRef" :can-cancel="false" :is-full-page="true"/>
    <div class="container-fluid">
        <div class="row">
            <div class="col-lg-6 col-md-12 order-md-3">
                <p v-if="loadingRef" class="text-secondary text-center">Loading collection...</p>
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
    <!-- Modal -->
    <div class="modal fade" id="newDeckModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="newDeckModalTitle">Create a New Deck</h1>
                    <button type="button" class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <div class="form-floating my-3">
                        <input type="text" class="form-control" id="floatingInput" placeholder="Deck Name" label="Deck Name" v-model="deckName">
                        <label for="floatingInput">Deck Name</label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onCreateDeck()">Create</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
#form-container {
    height: 100%;
}
</style>