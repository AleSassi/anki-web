import { DatalessResponse } from "../model/dataless_resp_model";
import { CollectionData, DeckData } from "../model/collection_model";
import { computed, ref, type Ref } from "vue";
import { BaseController } from "./base_controller";
import { DeckBrowseResponse, CardData, NoteData, NoteFieldData } from "@/model/card_model";
import HomeController from "./home_controller";

const myRef = ref(null);

interface ICardAddController {
    addCard(did: number, model_id: number, data: { [id: string]: string }): Promise<boolean>;
    uploadFile(did: number, model_id: number, file: any): Promise<boolean>;
}

export class CardAddController extends BaseController<DatalessResponse | null> implements ICardAddController {

    async addCard(did: number, model_id: number, data: { [id: string]: string; }): Promise<boolean> {
        let fields: NoteFieldData[] = [];
        for (let key in data) {
            fields.push(new NoteFieldData(key, data[key]));
        }
        let post_body = {
            deck_id: did,
            model_id: model_id,
            fields: fields
        }
        const res = await super.put<DatalessResponse>("/cards", {
            body: post_body,
            message: "Card added successfully"
        });
        if (res) {
            return true;
        }
        return false;
    }

    async uploadFile(did: number, model_id: number, file: any): Promise<boolean> {
        var formData = new FormData();
        formData.append("file", file.files[0]);
        // formData.append("document", documentJson); instead of this, use the line below.
        formData.append("document", JSON.stringify({
            deck_id: did,
            model_id: model_id
        }));

        const res = await super.put<DatalessResponse>("/cards/import-file", {
            body: formData,
            message: "Cards added successfully"
        })

        if (res) {
            return true;
        }
        return false;
    }

    getRef(): Ref<DatalessResponse | null> {
        return myRef;
    }

}

export default new CardAddController();