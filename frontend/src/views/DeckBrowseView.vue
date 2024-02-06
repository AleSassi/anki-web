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
import DeckBrowseController from '@/controllers/deck_browse_controller';
import DeckBrowseList from '@/components/DeckBrowseList.vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';

const deckData = HomeController.getOpenDeck();
const cardData = DeckBrowseController.getRef();
const cardList = ref<InstanceType<typeof DeckBrowseList> | null>(null);
const loadingRef = ref(true);

onMounted(async () => {
    if (!deckData.value) {
        await router.replace(RoutingPath.HOME);
        return;
    }

    loadingRef.value = true;
    const res = await DeckBrowseController.getCards(HomeController.getOpenDeckID());
    loadingRef.value = false;
    if (cardList.value) {
        cardList.value.displayedData = res?.cards ?? [];
    }
})

</script>

<template>
    <NavBar active_index="-1" />
    <div class="container">
    	<div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
    		<div class="col-lg-6 col-md-12 order-md-3">
    			<div><h2>{{ deckData?.name }}</h2></div>
    			<div class="my-3">
    				<div class="form-actions mb-2">
    					<button id="study_button" type="submit" @click="router.push(RoutingPath.DECK_DETAIL)" class="btn btn-primary rounded mx-3 d-inline-block">Back</button>
    				</div>
    			</div>
                <loading v-model:active="loadingRef" :can-cancel="false" :is-full-page="true"/>
                <DeckBrowseList ref="cardList"/>
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

<style scoped>#form-container {
    height: 100%;
}</style>