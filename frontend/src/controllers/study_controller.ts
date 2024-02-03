import type { DatalessResponse } from "../model/dataless_resp_model";
import { computed, ref, type Ref } from "vue";
import { BaseController } from "./base_controller";
import { StudyCardResponse, StudyCardData, CountsData, ButtonData, QuestionAnswerData, AnswerCardReply } from "@/model/study_card_model";
import HomeController from "./home_controller";

let reference = ref<StudyCardData | null>(null);

interface IStudyController {
    getCard(): Promise<StudyCardResponse | null>;
    answerCard(answerID: number): Promise<boolean>;
    setStudyingCard(newCard: StudyCardData | null): void;
}

export class StudyController extends BaseController<StudyCardData | null> implements IStudyController {

    async getCard(): Promise<StudyCardResponse | null> {
        const res = await super.get<StudyCardResponse>("/deck/study", {
            query: {
                deck_id: HomeController.getOpenDeck().value?.did
            }
        });
        if (res) {
            this.setStudyingCard(res.card_data ?? null);
            return res;
        }
        return null;
    }

    async answerCard(answerID: number): Promise<boolean> {
        const res = await super.post<AnswerCardReply>("/deck/study", {
            body: {
                deck_id: HomeController.getOpenDeck().value?.did,
                answer_id: answerID
            }
        });
        if (res) {
            if (res.answered) {
                this.setStudyingCard(null);
            }
            return res.answered;
        }
        return false;
    }

    setStudyingCard(newCard: StudyCardData | null): void {
        reference.value = newCard;
        if (newCard) {
            localStorage.setItem("studyingCard", JSON.stringify(newCard));
        } else {
            localStorage.removeItem("studyingCard");
        }
    }

    /**
     * Return the object reference of this controller. The controller is a singleton, so the reference is the same for all the class
     */
    getRef(): Ref<StudyCardData | null> {
        return reference;
    }

}

export default new StudyController();