<template>
    <div class="col">
        <div :class="card_class">
            <div :class="header_class">
                <h4 class="my-0 font-weight-normal">{{ title }}: </h4>
            </div>
            <div class="card-body">
                <h1 class="card-title pricing-card-title">{{ count }} <small class="text-muted">{{ count == 1 ? "Card" : "Cards" }}</small></h1>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import RoutingPath from '@/router/routing_path';
import { onMounted, ref, watch } from 'vue';
import { computed } from 'vue';
import HomeController from '@/controllers/home_controller';

interface Props {
    card_type: number; //0 = new, 1 = learn, 2 = review
}

const deckData = HomeController.getOpenDeck();
const props = defineProps<Props>();

const title = computed(() => {
    const titles = ["New", "To Learn", "To Review"];
    const idx = Math.max(Math.min(props.card_type, titles.length - 1), 0);
    return titles[idx];
})

const count = computed(() => {
    const counts = [deckData.value?.new_cards, deckData.value?.lrn_cards, deckData.value?.due_cards];
    const idx = Math.max(Math.min(props.card_type, counts.length - 1), 0);
    return counts[idx] ?? 0;
})

const card_class = computed(() => {
    const classes = ["primary", "warning", "success"];
    const idx = Math.max(Math.min(props.card_type, classes.length - 1), 0);
    return "card mb-4 box-shadow border-" + classes[idx] + " rounded";
})

const header_class = computed(() => {
    const classes = ["primary", "warning", "success"];
    const idx = Math.max(Math.min(props.card_type, classes.length - 1), 0);
    return "card-header text-bg-" + classes[idx] + " border-" + classes[idx];
})
</script>