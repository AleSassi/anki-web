import type { DatalessResponse } from "../model/dataless_resp_model";
import { CollectionData, DeckData } from "../model/collection_model";
import { computed, ref, type Ref } from "vue";
import { BaseController } from "./base_controller";

let reference = ref<CollectionData | null>(null);
let openDeckRef = ref<DeckData | null>(null);

interface IHomeController {
    openDeck(did: number): void;
    closeDeck(): void;
    createDeck(name: string): Promise<boolean>;
    deleteDeck(did: number): Promise<boolean>;
    uploadCollection(file: File): Promise<boolean>;
    getOpenDeck(): Ref<DeckData | null>;
    getOpenDeckID(): number;
    getDecks(): Promise<CollectionData | null>;
    setCollection(newCollection: CollectionData | null): void;
}

export class HomeController extends BaseController<CollectionData | null> implements IHomeController {

    isAuthenticated = computed(() => reference.value != null);

    async getDecks(): Promise<CollectionData | null> {
        const res = await super.get<CollectionData>("/collection");
        if (res) {
            this.setCollection(res);
            return res;
        }
        return null;
    }

    async createDeck(name: string): Promise<boolean> {
        const res = await super.post<DatalessResponse>("/deck/create", {
            body: {
                name: name
            },
            message: "Deck created successfully"
        });
        return res != null;
    }

    async uploadCollection(file: File): Promise<boolean> {
        var formData = new FormData();
        formData.append("file", file);

        const res = await super.put<DatalessResponse>("/collection", {
            body: formData,
            message: "Collection uploaded successfully",
            config: {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        })

        if (res) {
            return true;
        }
        return false;
    }

    async deleteDeck(did: number): Promise<boolean> {
        const res = await super.delete("/deck", {
            body: {
                deck_id: did
            },
            message: "Deck deleted successfully"
        });
        return res;
    }

    openDeck(did: number): void {
        localStorage.setItem("openDeck", JSON.stringify({"did": did}));
    }

    getOpenDeck(): Ref<DeckData | null> {
        let openDeckId = JSON.parse(localStorage.getItem("openDeck") ?? '{"did": -1}').did;
        if (openDeckId == -1 || !reference.value) {
            openDeckRef.value = null;
        } else {
            openDeckRef.value = this.findDeckData(openDeckId, reference.value.decks);
        }

        return openDeckRef;
    }

    getOpenDeckID(): number {
        return JSON.parse(localStorage.getItem("openDeck") ?? '{"did": -1}').did;
    }

    closeDeck() {
        localStorage.removeItem("openDeck");
        openDeckRef.value = null;
    }

    setCollection(newCollection: CollectionData | null): void {
        reference.value = newCollection;
        if (newCollection) {
            localStorage.setItem("collection", JSON.stringify(newCollection));
        } else {
            localStorage.removeItem("collection");
        }
    }
    
    /**
     * Return the object reference of this controller. The controller is a singleton, so the reference is the same for all the class
     */
    getRef(): Ref<CollectionData | null> {
        return reference;
    }

    findDeckData(did: number, decks: DeckData[]): DeckData | null {
        for (let index = 0; index < decks.length; index++) {
            const deck = decks[index];
            if (deck.did == did) {
                return deck;
            } else if (deck.children.length > 0) {
                let child_find = this.findDeckData(did, deck.children);
                if (child_find) {
                    return child_find;
                }
            }
        }
        return null;
    }

}

export default new HomeController();