export class DeckData {
    name: string;
    did: number;
    new_cards: number;
    due_cards: number;
    lrn_cards: number;
    children: Array<DeckData>;

    constructor(name: string, did: number, new_cards: number, due_cards: number, lrn_cards: number, children: Array<DeckData>) {
        this.name = name;
        this.did = did;
        this.new_cards = new_cards;
        this.due_cards = due_cards;
        this.lrn_cards = lrn_cards;
        this.children = children;
    }
}

export class CollectionData {
    decks: Array<DeckData>;
    studiedCards: number;
    studiedTime: number;

    constructor(decks: Array<DeckData>, studiedCards: number, studiedTime: number) {
        this.decks = decks;
        this.studiedCards = studiedCards;
        this.studiedTime = studiedTime;
    }
}