/*
* Adapted from https://github.com/PrivTap/PrivTap
*/

import type { ErrorResponse } from "../model/error_model";
import type { AxiosError } from "axios";
import { useToast } from "vue-toastification";

export default function axiosCatch(error: any): void {
    const err = error as AxiosError;
    var message = "An error occured";
    if (err.response?.data) {
        message = (err.response?.data as ErrorResponse<Object>).detail;
    }
    useToast().error(message);
}