export class QuestionAnswerData {
    html_text: string;
    sounds: any[];

    constructor(html_text: string, sounds: any[]) {
        this.html_text = html_text;
        this.sounds = sounds;
    }
}

export class ButtonData {
    id: number;
    title: string;
    interval: string;

    constructor(id: number, title: string, interval: string) {
        this.id = id;
        this.title = title;
        this.interval = interval;
    }
}

export class CountsData {
    unseen: number;
    learning: number;
    revising: number;

    constructor(unseen: number, learning: number, revising: number) {
        this.unseen = unseen;
        this.learning = learning;
        this.revising = revising;
    }
}

export class StudyCardData {
    question: QuestionAnswerData;
    answer: QuestionAnswerData;
    buttons: Array<ButtonData>;
    card_type: number;
    counts: CountsData;
    
    constructor(question: QuestionAnswerData, answer: QuestionAnswerData, buttons: Array<ButtonData>, card_type: number, counts: CountsData) {
        this.question = question;
        this.answer = answer;
        this.buttons = buttons;
        this.card_type = card_type;
        this.counts = counts;
    }
}

export class StudyCardResponse {
    finished: boolean;
    card_data?: StudyCardData;

    constructor(finished: boolean, card_data?: StudyCardData) {
        this.finished = finished;
        this.card_data = card_data;
    }
}

export class AnswerCardReply {
    answered: boolean

    constructor(answered: boolean) {
        this.answered = answered;
    }
}