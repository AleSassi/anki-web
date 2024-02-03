<template>
    <li class="rounded mb-2 list-group-item list-group-item-action d-flex justify-content-between align-items-center" @click="openDeck">
        <span class="fw-medium">{{ props.title }}</span>
        <span>
            <span class="badge text-bg-primary rounded-pill mx-05">{{ props.lrn_count }}</span>
            <span class="badge text-bg-danger rounded-pill mx-05">{{ props.rev_count }}</span>
            <span class="badge text-bg-success rounded-pill mx-05">{{ props.new_count }}</span>
        </span>
    </li>
    <DeckList class="reduced-margin" v-if="children.length > 0" ref="childList"/>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import RoutingPath from '@/router/routing_path';
import { onMounted, ref, watch } from 'vue';
import { computed } from 'vue';
import type { DeckData } from '@/model/collection_model';
import DeckList from './DeckList.vue';
import HomeController from '@/controllers/home_controller';

interface Props {
    title: string;
    new_count: number;
    rev_count: number;
    lrn_count: number;
    deck_id: number;
    children: DeckData[];
}

const props = defineProps<Props>();
const router = useRouter();
const childList = ref<InstanceType<typeof DeckList> | null>(null);

onMounted(() => {
    if (childList.value) {
        childList.value.displayedData = props.children;
    }
})

function openDeck() {
    let did = props.deck_id;
    HomeController.openDeck(did);
    router.replace(RoutingPath.DECK_DETAIL);
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