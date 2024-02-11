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
const cardData = DeckBrowseController.getOpenCard();
const loadingRef = ref(true);

let fieldHashMap = ref<{ [id: string]: string }>({});

onMounted(async () => {
    if (!cardData.value) {
        await router.replace(RoutingPath.HOME);
        return;
    }

    for (let i = 0; i < (cardData.value.note?.fields ?? []).length; i++) {
        const element = cardData.value.note?.fields[i];
        if (element) {
            fieldHashMap.value[element.name] = element.value;
        }
    }
})

async function onSubmitted(event: Event) {
    loadingRef.value = true;
    if (event) {
        event.preventDefault();
    }

    const res = await DeckBrowseController.editOpenCard(fieldHashMap.value);
    if (res && deckData.value?.did) {
        DeckBrowseController.closeCard();
        await DeckBrowseController.getCards(deckData.value.did);

        if (cardData.value) {
            for (let i = 0; i < (cardData.value.note?.fields ?? []).length; i++) {
                const element = cardData.value.note?.fields[i];
                if (element) {
                    fieldHashMap.value[element.name] = element.value;
                }
            }
        } else {
            await router.replace(RoutingPath.HOME);
            return;
        }
    }
    loadingRef.value = false;
}

async function onDelete(event: Event) {
    loadingRef.value = true;
    if (event) {
        event.preventDefault();
    }

    const res = await DeckBrowseController.deleteOpenCard();
    if (res && deckData.value?.did) {
        DeckBrowseController.closeCard();
        await DeckBrowseController.getCards(deckData.value.did);

        await router.replace(RoutingPath.DECK_BROWSE);
    }
    loadingRef.value = false;
}

</script>

<template>
    <NavBar active_index="-1" />
    <div class="container">
        <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
            <div class="col-lg-6 col-md-12 order-md-3">
                <div>
                    <h2>Edit Card</h2>
                </div>
                <div class="my-3">
                    <div class="form-actions mb-2">
                        <button id="study_button" type="submit" @click="router.push(RoutingPath.DECK_BROWSE)"
                            class="btn btn-primary rounded mx-3 d-inline-block">Back</button>
                    </div>
                </div>
                <form>
                    <div v-for="field in cardData?.note?.fields ?? []" class="form-floating my-3">
                        <input type="text" class="form-control" :id="field.name" :placeholder="field.value" v-model="fieldHashMap[field.name]">
                        <label :for="field.name">{{ field.name }}</label>
                    </div>
                    <div class="my-3">
                        <div class="form-actions mb-2">
                            <button class="btn btn-primary rounded py-2 mx-3 d-inline-block" type="submit" @click="onSubmitted($event)">Edit Card</button>
                            <button class="btn btn-danger rounded py-2 mx-3 d-inline-block" type="button" @click="onDelete($event)">Delete Card</button> <!-- @click="onSubmitted($event)">{{ showLogin ? "Sign in" : "Sign up" }}</button> -->
                        </div>
                    </div>
    			</form>
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