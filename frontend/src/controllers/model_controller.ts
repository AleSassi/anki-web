import type { DatalessResponse } from "../model/dataless_resp_model";
import type { ModelListResponse, ModelResponse, AnkiModel, AnkiModelEntry } from "../model/ankimodel_model";
import { CollectionData, DeckData } from "../model/collection_model";
import { computed, ref, type Ref } from "vue";
import { BaseController } from "./base_controller";

let reference = ref<ModelListResponse | null>(null);

interface IModelController {
    getModelList(): Promise<ModelListResponse | null>
    getModel(mid: number): Promise<ModelResponse | null>
    setModelList(newList: ModelListResponse | null): void;
}

export class ModelController extends BaseController<ModelListResponse | null> implements IModelController {

    async getModelList(): Promise<ModelListResponse | null> {
        const res = await super.get<ModelListResponse>("/collection/models");
        if (res) {
            this.setModelList(res);
            return res;
        }
        return null;
    }

    async getModel(mid: number): Promise<ModelResponse | null> {
        const res = await super.get<ModelResponse>("/collection/models", {
            query: {
                model_id: mid
            }
        });
        return res;
    }

    setModelList(newList: ModelListResponse | null): void {
        reference.value = newList;
    }

    /**
     * Return the object reference of this controller. The controller is a singleton, so the reference is the same for all the class
     */
    getRef(): Ref<ModelListResponse | null> {
        return reference;
    }

}

export default new ModelController();