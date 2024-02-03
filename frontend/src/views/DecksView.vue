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

const deckData = HomeController.getRef();
const deckList = ref<InstanceType<typeof DeckList> | null>(null);
const loading = ref(true);

onMounted(async () => {
    const res = await HomeController.getDecks();
    loading.value = false;
    if (deckList.value) {
        console.log("Setting")
        deckList.value.displayedData = res?.decks ?? [];
    }
})
</script>

<template>
    <NavBar active_index="0" />

    <div class="container-fluid">
        <div class="row">
            <div class="col-lg-6 col-md-12 order-md-3">
                <p v-if="loading" class="text-secondary text-center">Loading collection</p>
                <DeckList ref="deckList"/>
                <!--
                <ul class="list-group">
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1679949929819')">
                      <span>Core 2000</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">15</span>
    					  <span class="badge text-bg-danger rounded-pill">4</span>
    					  <span class="badge text-bg-success rounded-pill">184</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1678219975191')">
                      <span>Custom Study Session</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">0</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">0</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1677792678989')">
                      <span>Japanese Core 2000 Step 01 Listening Sentence Vocab + Images</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">15</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">1</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1678120430000')">
                      <span>Japanese Course Kyoko B2</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">0</span>
    					  <span class="badge text-bg-danger rounded-pill">12</span>
    					  <span class="badge text-bg-success rounded-pill">23</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1678575055559')">
                      <span>JLPT Tango N4 Alpha</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">15</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">30</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1677794123971')">
                      <span>JLPT Tango N5 MIA Japanese</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">15</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">100</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1678093841384')">
                      <span>Open Anki JLPT N4 Deck</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">15</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">0</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1690395839935')">
                      <span>Pass JLPT N3 Kanji Deck</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">10</span>
    					  <span class="badge text-bg-danger rounded-pill">2</span>
    					  <span class="badge text-bg-success rounded-pill">37</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1690395830676')">
                      <span>Pass JLPT N3 Vocabulary Deck</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">15</span>
    					  <span class="badge text-bg-danger rounded-pill">16</span>
    					  <span class="badge text-bg-success rounded-pill">66</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1678142384721')">
                      <span>Pass JLPT N4 Kanji Deck</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">0</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">10</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1678142392909')">
                      <span>Pass JLPT N4 Vocabulary Deck</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">0</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">64</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1677792795105')">
                      <span>Pass JLPT N5 Kanji Deck</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">0</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">0</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1677795136883')">
                      <span>Ultimate JLPT N5 Vocabulary Deck v1.2</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">0</span>
    					  <span class="badge text-bg-danger rounded-pill">0</span>
    					  <span class="badge text-bg-success rounded-pill">22</span>
    				  </span>
                    </li>
                    
                
                    <li class="rounded mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328803940')">
                      <span>日本語能力試験 N3</span>
    				  <span>
    					  <span class="badge text-bg-primary rounded-pill">0</span>
    					  <span class="badge text-bg-danger rounded-pill">4</span>
    					  <span class="badge text-bg-success rounded-pill">77</span>
    				  </span>
                    </li>
                    
                        <li class="rounded ms-5 mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328695823')">
                          <span>Adverbs</span>
                          <span>
    						  <span class="badge text-bg-primary rounded-pill">0</span>
    						  <span class="badge text-bg-danger rounded-pill">0</span>
    						  <span class="badge text-bg-success rounded-pill">11</span>
    					  </span>
                        </li>
                    
                        <li class="rounded ms-5 mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328590477')">
                          <span>する動詞</span>
                          <span>
    						  <span class="badge text-bg-primary rounded-pill">0</span>
    						  <span class="badge text-bg-danger rounded-pill">2</span>
    						  <span class="badge text-bg-success rounded-pill">17</span>
    					  </span>
                        </li>
                    
                        <li class="rounded ms-5 mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328770955')">
                          <span>その他の語彙</span>
                          <span>
    						  <span class="badge text-bg-primary rounded-pill">0</span>
    						  <span class="badge text-bg-danger rounded-pill">0</span>
    						  <span class="badge text-bg-success rounded-pill">4</span>
    					  </span>
                        </li>
                    
                        <li class="rounded ms-5 mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328576462')">
                          <span>動詞</span>
                          <span>
    						  <span class="badge text-bg-primary rounded-pill">0</span>
    						  <span class="badge text-bg-danger rounded-pill">2</span>
    						  <span class="badge text-bg-success rounded-pill">22</span>
    					  </span>
                        </li>
                    
                        <li class="rounded ms-5 mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328711734')">
                          <span>名詞</span>
                          <span>
    						  <span class="badge text-bg-primary rounded-pill">0</span>
    						  <span class="badge text-bg-danger rounded-pill">0</span>
    						  <span class="badge text-bg-success rounded-pill">7</span>
    					  </span>
                        </li>
                    
                        <li class="rounded ms-5 mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328614417')">
                          <span>形容詞</span>
                          <span>
    						  <span class="badge text-bg-primary rounded-pill">0</span>
    						  <span class="badge text-bg-danger rounded-pill">0</span>
    						  <span class="badge text-bg-success rounded-pill">6</span>
    					  </span>
                        </li>
                    
                        <li class="rounded ms-5 mb-2 list-group-item d-flex justify-content-between align-items-center list-group-item-primary" onclick="jump_to_page('/ankiweb/decks/overview/1695328486814')">
                          <span>漢字</span>
                          <span>
    						  <span class="badge text-bg-primary rounded-pill">0</span>
    						  <span class="badge text-bg-danger rounded-pill">0</span>
    						  <span class="badge text-bg-success rounded-pill">10</span>
    					  </span>
                        </li>
                    
                
                    </ul>
                    <div>It took None seconds to learn 0 cards today.</div>
                    -->
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