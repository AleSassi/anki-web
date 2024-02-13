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
import DeckDetailContainer from '@/components/DeckDetailContainer.vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';
import { useToast } from 'vue-toastification';

const loadingRef = ref(false);
const deckData = HomeController.getOpenDeck();

onMounted(async () => {
	if (deckData.value == null) {
		router.replace(RoutingPath.HOME);
	}
})

const deckFinished = computed(() => {
	return deckData.value?.due_cards == 0 && deckData.value?.lrn_cards == 0 && deckData.value?.new_cards == 0
})

function study() {
	router.replace(RoutingPath.DECK_STUDY);
}

function browse() {
	router.replace(RoutingPath.DECK_BROWSE);
}

function stats() {
	router.replace(RoutingPath.DECK_STATS);
}

function settings() {
	router.replace(RoutingPath.DECK_SETTINGS);
}

function add_cards() {
	router.replace(RoutingPath.DECK_ADD_CARDS);
}

async function delete_deck() {
	loadingRef.value = true;
	if (deckData.value == null) {
		router.replace(RoutingPath.HOME);
		useToast().error("No open deck was found");
		return;
	}

	const res = await HomeController.deleteDeck(deckData.value.did);
	if (res) {
		router.replace(RoutingPath.HOME);
	}
	loadingRef.value = false;
}

function home() {
	HomeController.closeDeck();
	router.replace(RoutingPath.HOME);
}

</script>

<template>
	<NavBar active_index="-1" />
	<loading v-model:active="loadingRef" :can-cancel="false" :is-full-page="true"/>
	<div class="container">
		<div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
			<div class="col-lg-6 col-md-12 order-md-3">
				<div><h2>{{ deckData?.name }}</h2></div>
				<div><div class="mb-2"></div></div>
				
				<div>
					<div class="mb-2" v-if="deckFinished">
						<b>Congratulations! Today's portion of the deck has been completed.</b>
					</div>
					<div class="form-actions mb-2">
						<button id="study_button" @click="home" class="btn btn-primary rounded mx-3 my-2 d-inline-block" v-if="deckFinished">Home</button>
						<button id="study_button" @click="study" class="btn btn-primary rounded mx-3 my-2 d-inline-block" v-if="!deckFinished">Start</button>
						<button id="browse_button" @click="browse" class="btn btn-secondary rounded mx-3 my-2 d-inline-block" type="button">Browse</button>
						<button id="stats_button" @click="stats" class="btn btn-secondary rounded mx-3 my-2 d-inline-block" type="button">Stats</button>
						<button id="settings_button" @click="settings" class="btn btn-info rounded mx-3 my-2 d-inline-block">Settings</button>
						<button id="add_button" @click="add_cards" class="btn btn-success rounded mx-3 my-2 d-inline-block" type="button">Add Cards</button>
						<button id="del_button" @click="delete_deck" class="btn btn-danger rounded mx-3 my-2 d-inline-block" type="button">Delete Deck</button>
					</div>
			  	</div>

				<DeckDetailContainer v-if="!deckFinished" />
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