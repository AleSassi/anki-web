import type { DatalessResponse } from "../model/dataless_resp_model";
import { CollectionData } from "../model/collection_model";
import { computed, ref, type Ref } from "vue";
import { BaseController } from "./base_controller";

let reference = ref<CollectionData | null>(null);

interface IHomeController {
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

}

export default new HomeController();