<template>
    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-action" @click="openCard">
    	<!-- This is the first field of note.items() -->
    	<span class="fw-medium">{{ props.title }}</span>
        <span>
            <!-- This is Forward if card.ord == 0, otheriwse Reverse -->
            <span class="me-2 text-secondary-emphasis">{{ props.card_type }}</span>
            <!-- This is the card state, either New, Learned or Study -->
            <span class="me-2 text-secondary-emphasis">{{ props.card_state }}</span>
        </span>
    </li>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import RoutingPath from '@/router/routing_path';
import { onMounted, ref, watch } from 'vue';
import { computed } from 'vue';
import type { DeckData } from '@/model/collection_model';
import DeckBrowseController from '@/controllers/deck_browse_controller';

interface Props {
    title: string;
    card_type: string;
    card_state: string;
    card_id: number;
}

const props = defineProps<Props>();
const router = useRouter();

onMounted(() => {
})

function openCard() {
    let cid = props.card_id;
    DeckBrowseController.openCard(cid);
    router.replace(RoutingPath.CARD_DETAIL);
}

</script>

<style scoped>
.mx-05 {
    margin-left: 0.1rem !important;
    margin-right: 0.1rem !important;
}

.reduced-margin {
    margin-left: 3rem !important;
}
</style>