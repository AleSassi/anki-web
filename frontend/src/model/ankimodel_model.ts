export class ModelField {
    name: string;
    ord: number;
    sticky: boolean;
    rtl: boolean;
    font: string;
    size: number;
    description: string;
    plainText: boolean;
    collapsed: boolean;
    excludeFromSearch: boolean;

    constructor(name: string, ord: number, sticky: boolean, rtl: boolean, font: string, size: number, description: string, plainText: boolean, collapsed: boolean, excludeFromSearch: boolean) {
        this.name = name;
        this.ord = ord;
        this.sticky = sticky;
        this.rtl = rtl;
        this.font = font;
        this.size = size;
        this.description = description;
        this.plainText = plainText;
        this.collapsed = collapsed;
        this.excludeFromSearch = excludeFromSearch;
    }
}

export class AnkiModel {
    id: string;
    name: string;
    type: number;
    mod: number;
    usn: number;
    sortf: number;
    did: number;
    flds: Array<ModelField>;

    constructor(id: string, name: string, type: number, mod: number, usn: number, sortf: number, did: number, flds: Array<ModelField>) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.mod = mod;
        this.usn = usn;
        this.sortf = sortf;
        this.did = did;
        this.flds = flds;
    }
}

export class AnkiModelEntry {
    name: string;
    id: number;

    constructor(name: string, id: number) {
        this.name = name;
        this.id = id;
    }
}

export class ModelListResponse {
    models: Array<AnkiModelEntry>;

    constructor(models: Array<AnkiModelEntry>) {
        this.models = models;
    }
}

export class ModelResponse {
    model: AnkiModel;

    constructor(model: AnkiModel) {
        this.model = model;
    }
}