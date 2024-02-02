export class ErrorResponse<T extends Object> {
    detail: string;

    constructor(detail: string) {
        this.detail = detail;
    }
}