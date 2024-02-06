export class NoteFieldData {
    name: string;
    value: string;

    constructor(name: string, value: string) {
        this.name = name;
        this.value = value;
    }
}

export class NoteData {
    id: number;
    guid: string;
    model_id: number;
    last_modified: number;
    usn: number;
    tags: Array<string>;
    fields: Array<NoteFieldData>;

    constructor(id: number, guid: string, model_id: number, last_modified: number, usn: number, tags: Array<string>, fields: Array<NoteFieldData>) {
        this.id = id;
        this.guid = guid;
        this.model_id = model_id;
        this.last_modified = last_modified;
        this.usn = usn;
        this.tags = tags;
        this.fields = fields;
    }
}

export class CardData {
    note?: NoteData;
    lastIvl: number;
    ord: string;
    nid: number;
    id: number;
    did: number;
    odid: number;
    queue: number;
    type: string;

    constructor(lastIvl: number, ord: string, nid: number, id: number, did: number, odid: number, queue: number, type: string, note?: NoteData) {
        this.note = note;
        this.lastIvl = lastIvl;
        this.ord = ord;
        this.nid = nid;
        this.id = id;
        this.did = did;
        this.odid = odid;
        this.queue = queue;
        this.type = type;
    }
}

export class DeckBrowseResponse {
    cards: Array<CardData>;

    constructor(cards: Array<CardData>) {
        this.cards = cards;
    }
}