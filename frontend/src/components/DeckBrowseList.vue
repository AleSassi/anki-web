<template>
    <ul class="list-group">
        <DeckBrowseEntry v-for="card in displayedData" :title="card.note?.fields[0].value ?? 'undefined'" :card_id="card.id" :card_type="card.type"
            :card_state="card.ord" />
    </ul>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import RoutingPath from '@/router/routing_path';
import HomeController from '@/controllers/home_controller';
import { onMounted, ref, watch } from 'vue';
import { computed } from 'vue';
import { DeckBrowseResponse, CardData, NoteData, NoteFieldData } from "@/model/card_model";
import DeckBrowseEntry from './DeckBrowseEntry.vue';

var displayedData = ref<Array<CardData>>([]);

defineExpose({
    displayedData
})
const router = useRouter();
</script>