<template>
    <ul class="list-group">
        <DeckEntry v-for="deck in displayedData" :title="deck.name" :deck_id="deck.did" :new_count="deck.new_cards" :lrn_count="deck.lrn_cards" :rev_count="deck.due_cards" :children="deck.children"/>
    </ul>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import RoutingPath from '@/router/routing_path';
import HomeController from '@/controllers/home_controller';
import { onMounted, ref, watch } from 'vue';
import { computed } from 'vue';
import { DeckData } from '@/model/collection_model';
import DeckEntry from './DeckEntry.vue';

var displayedData = ref<Array<DeckData>>([]);

defineExpose({
    displayedData
})
const router = useRouter();
</script>