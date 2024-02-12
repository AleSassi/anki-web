<script setup lang="ts">
import TextField from '../components/TextField.vue'
import NavBar from '@/components/NavBar.vue';
import logoURL from '../assets/logo.svg'
import AuthController from '../controllers/auth_controller'
import { ref, computed } from "vue";
import router from "@/router/index";
import RoutingPath from "@/router/routing_path";
import HomeController from '@/controllers/home_controller';
import ModelController from '@/controllers/model_controller';
import DeckList from '@/components/DeckList.vue';
import DeckEntry from '@/components/DeckEntry.vue';
import { onMounted } from 'vue';
import { CollectionData } from '@/model/collection_model';
import DeckDetailContainer from '@/components/DeckDetailContainer.vue';
import DeckBrowseController from '@/controllers/deck_browse_controller';
import DeckBrowseList from '@/components/DeckBrowseList.vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';
import { useToast } from 'vue-toastification';
import { ModelResponse } from '@/model/ankimodel_model';
import CardAddController from '@/controllers/card_add_controller';

const deckData = HomeController.getOpenDeck();
const modelListDataRef = ModelController.getRef();
const selectedModelID = ref<number | null>(null);
const modelData = ref<ModelResponse | null>(null);
const loadingRef = ref(true);

let fieldHashMap = ref<{ [id: string]: string }>({});

onMounted(async () => {
    if (!deckData.value) {
        await router.replace(RoutingPath.HOME);
        return;
    }

    loadingRef.value = true;
    const res = await ModelController.getModelList();
    if (!res) {
        await router.replace(RoutingPath.HOME);
        loadingRef.value = false;
        return;
    }
    loadingRef.value = false;
})

async function onSubmitted(event: Event) {
    loadingRef.value = true;
    if (event) {
        event.preventDefault();
    }

    if (deckData.value?.did && selectedModelID.value) {
        const res = await CardAddController.addCard(deckData.value.did, selectedModelID.value, fieldHashMap.value);
        for (let i = 0; i < (modelData.value?.model.flds ?? []).length; i++) {
            const element = modelData.value?.model.flds[i];
            if (element) {
                fieldHashMap.value[element.name] = "";
            }
        }
    }
    loadingRef.value = false;
}

async function onModelSelection(event: Event) {
    loadingRef.value = true;
    if (event) {
        event.preventDefault();
    }

    if (selectedModelID.value) {
        const res = await ModelController.getModel(selectedModelID.value);
        modelData.value = res;
        if (res) {
            fieldHashMap.value = {};
            for (let i = 0; i < (res.model.flds ?? []).length; i++) {
                const element = res.model.flds[i];
                if (element) {
                    fieldHashMap.value[element.name] = "";
                }
            }
        }
    } else {
        useToast().error("No model ID selected");
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
                    <h2>Add Cards</h2>
                </div>
                <div class="my-3">
                    <div class="form-actions mb-2">
                        <button id="study_button" type="submit" @click="router.push(RoutingPath.DECK_BROWSE)"
                            class="btn btn-primary rounded mx-3 d-inline-block">Back</button>
                    </div>
                </div>
                <div class="form-check my-3">
                    <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                    <label class="form-check-label" for="flexCheckDefault">
                        Upload from CSV file
                    </label>
                </div>
                <form>
                    <loading v-model:active="loadingRef" :can-cancel="false" :is-full-page="true"/>
                    <select class="form-select my-3" required @change="onModelSelection($event)" v-model="selectedModelID">
                        <option selected>Select Card Model</option>
                        <option v-for="model in modelListDataRef?.models" :value="model.id">{{ model.name }}</option>
                    </select>
                    <div v-for="field in modelData?.model.flds ?? []" class="form-floating my-3">
                        <input type="text" class="form-control" :id="field.name" v-model="fieldHashMap[field.name]">
                        <label :for="field.name">{{ field.name }}</label>
                    </div>
                    <div class="my-3">
                        <div class="form-actions mb-2">
                            <button class="btn btn-primary rounded py-2 mx-3 d-inline-block" type="submit"
                                @click="onSubmitted($event)" :disabled="!(deckData && selectedModelID)">Add Card</button>
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