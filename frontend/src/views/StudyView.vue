<script setup lang="ts">
import NavBar from '@/components/NavBar.vue';
import AuthController from '../controllers/auth_controller'
import { ref, computed } from "vue";
import router from "@/router/index";
import RoutingPath from "@/router/routing_path";
import HomeController from '@/controllers/home_controller';
import { onMounted } from 'vue';
import DeckDetailContainer from '@/components/DeckDetailContainer.vue';
import StudyController from '@/controllers/study_controller';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';

const cardData = StudyController.getRef();
const hideAnswer = ref<boolean>(true);
const loadingCard = ref<boolean>(true);

onMounted(async () => {
    const card = await StudyController.getCard();
    if (!card || card.finished) {
        router.replace(RoutingPath.DECK_DETAIL);
    } else {
        loadingCard.value = false;
    }
})

const newClass = computed(() => {
    return cardData.value?.card_type == 0 ? "text-decoration-underline" : "";
})

const lrnClass = computed(() => {
    return cardData.value?.card_type == 1 ? "text-decoration-underline" : "";
})

const dueClass = computed(() => {
    return cardData.value?.card_type == 2 ? "text-decoration-underline" : "";
})

function show_answer() {
    hideAnswer.value = false;
}

async function answer_card(btn: number) {
    loadingCard.value = true;
    const answered = await StudyController.answerCard(btn);
    if (answered) {
        hideAnswer.value = true;
        const card = await StudyController.getCard();
        if (!card || card.finished) {
            const openDeckID = HomeController.getOpenDeckID();
            HomeController.closeDeck();
            const decks = await HomeController.getDecks();
            HomeController.openDeck(openDeckID);
            loadingCard.value = false;
            router.replace(RoutingPath.DECK_DETAIL);
        } else {
            loadingCard.value = false;
        }
    } else {
        loadingCard.value = false;
    }
}

</script>

<template>
    <NavBar active_index="-1" />
    <div class="container">
        <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
            <div class="col-lg-6 col-md-12 order-md-3">
                <div class="card-card mb-3 text-center">
                    <loading v-model:active="loadingCard" :can-cancel="false" :is-full-page="false"/>
                    <div id="question_box" v-if="hideAnswer">
                        <div class="mb-4">
                            <div class="rounded card-header">
                                <h4 class="my-0 fw-bold">Question</h4>
                            </div>
                            <div class="rounded card-body" style="font-size: 24px" v-html="cardData?.question.html_text">
                            </div>
                        </div>
                        <div class="mx-auto my-4">
                            <span :class='"text-primary mx-3 " + newClass'>{{ cardData?.counts.unseen }}</span>
                            <span :class='"text-danger mx-3 " + lrnClass'>{{ cardData?.counts.learning }}</span>
                            <span :class='"text-success mx-3 " + dueClass'>{{ cardData?.counts.revising }}</span>
                        </div>  
                        <div class="rounded bg-body-secondary mb-4 box-shadow" @click="show_answer">
                            <div class="card-header">
                                <h4 class="my-3 py-2 font-weight-normal">Show answer</h4>
                            </div>
                        </div>
                    </div>
                    <div id="answer_box" v-if="!hideAnswer">
                        <div class="mb-4">
                            <div class="rounded card-header">
                                <h4 class="my-0 fw-bold">Answer</h4>
                            </div>
                            <div class="rounded card-body" style="font-size: 24px" v-html="cardData?.answer.html_text">
                            </div>
                        </div>
                        <div class="mx-auto my-4">
                            <span :class='"text-primary mx-3 " + newClass'>{{ cardData?.counts.unseen }}</span>
                            <span :class='"text-danger mx-3 " + lrnClass'>{{ cardData?.counts.learning }}</span>
                            <span :class='"text-success mx-3 " + dueClass'>{{ cardData?.counts.revising }}</span>
                        </div>
                        <div class="container">
                            <div class="row align-items-center">
                                <div v-for="btn in cardData?.buttons" class="col py-2 bg-body-secondary mb-4 box-shadow mx-3 rounded" @click="answer_card(btn.id)">
                                    <div class="card-header">
                                        <h4 class="my-0 font-weight-normal">{{ btn.title }}</h4>
                                        <p class="mt-2 mb-0 fs-6 fw-light text-secondary-emphasis">{{ btn.interval }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
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