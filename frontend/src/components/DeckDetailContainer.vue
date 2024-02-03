<template>
    <div class="card-deck my-3 text-center">
        <DeckDetailCard :card_type="0"/>
        <DeckDetailCard :card_type="1"/>
        <DeckDetailCard :card_type="2"/>
    </div>
</template>

<script setup lang="ts">
import DeckDetailCard from './DeckDetailCard.vue';

</script>