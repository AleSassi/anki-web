<script setup lang="ts">
import { ref } from 'vue'

defineProps(['type', 'placeholder', 'label', 'id', "json-name"])

var text_data: string = "";
</script>

<template>
    <div class="form-floating my-3">
        <input :type="type" class="form-control" :id="id" :placeholder="placeholder" v-model="text_data" @input="$emit('inputChanged', text_data)">
        <label :for="id">{{ label }}</label>
    </div>
</template>