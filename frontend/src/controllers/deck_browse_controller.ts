import { DatalessResponse } from "../model/dataless_resp_model";
import { CollectionData, DeckData } from "../model/collection_model";
import { computed, ref, type Ref } from "vue";
import { BaseController } from "./base_controller";
import { DeckBrowseResponse, CardData, NoteData, NoteFieldData } from "@/model/card_model";
import HomeController from "./home_controller";

let reference = ref<DeckBrowseResponse | null>(null);
let openCardRef = ref<CardData | null>(null);
let openCardId: number;

interface IDeckBrowseController {
    openCard(cid: number): void;
    closeCard(): void;
    getOpenCard(): Ref<CardData | null>;
    getOpenCardID(): number;
    getCards(did: number): Promise<DeckBrowseResponse | null>;
    setCards(newCards: DeckBrowseResponse | null): void;
    editOpenCard(data: { [id: string]: string }): Promise<boolean>;
    deleteOpenCard(): Promise<boolean>;
}

export class DeckBrowseController extends BaseController<DeckBrowseResponse | null> implements IDeckBrowseController {

    isAuthenticated = computed(() => reference.value != null);

    async getCards(did: number): Promise<DeckBrowseResponse | null> {
        const res = await super.get<DeckBrowseResponse>("/deck/cards", {
            query: {
                deck_id: HomeController.getOpenDeck().value?.did
            }
        });
        if (res) {
            this.setCards(res);
            return res;
        }
        return null;
    }

    async editOpenCard(data: { [id: string]: string }): Promise<boolean> {
        let fields: NoteFieldData[] = [];
        for (const field of openCardRef.value?.note?.fields ?? []) {
            fields.push(new NoteFieldData(field.name, data[field.name]));
        }
        let post_body = {
            card_id: openCardId,
            fields: fields
        }
        const res = await super.post<DatalessResponse>("/cards", {
            body: post_body,
            message: "Card edited successfully"
        });
        if (res) {
            return true;
        }
        return false;
    }

    async deleteOpenCard(): Promise<boolean> {
        let post_body = {
            card_ids: [openCardId]
        }
        const res = await super.delete("/cards", {
            body: post_body,
            message: "Card deleted successfully"
        });
        return res;
    }

    openCard(cid: number): void {
        openCardId = cid;
        //localStorage.setItem("openCard", JSON.stringify({ "cid": cid }));
    }

    getOpenCard(): Ref<CardData | null> {
        //let openCardId = JSON.parse(localStorage.getItem("openCard") ?? '{"cid": -1}').cid;
        if (openCardId == -1 || !reference.value) {
            openCardRef.value = null;
        } else {
            openCardRef.value = this.findCardData(openCardId, reference.value.cards);
        }

        return openCardRef;
    }

    getOpenCardID(): number {
        return openCardId;//JSON.parse(localStorage.getItem("openCard") ?? '{"cid": -1}').did;
    }

    closeCard(): void {
        localStorage.removeItem("openCard");
        openCardRef.value = null;
    }

    /**
     * Return the object reference of this controller. The controller is a singleton, so the reference is the same for all the class
     */
    getRef(): Ref<DeckBrowseResponse | null> {
        return reference;
    }

    setCards(newCards: DeckBrowseResponse | null): void {
        reference.value = newCards;
        /*if (newCards) {
            localStorage.setItem("cards", JSON.stringify(newCards));
        } else {
            localStorage.removeItem("cards");
        }*/
    }

    findCardData(cid: number, cards: CardData[]): CardData | null {
        for (let index = 0; index < cards.length; index++) {
            const card = cards[index];
            if (card.id == cid) {
                return card;
            }
        }
        return null;
    }

}

export default new DeckBrowseController();